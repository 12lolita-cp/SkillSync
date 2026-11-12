from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.database import users_collection
from app.schemas.student_schema import (
    StudentCreate,
    StudentUpdate
)

router = APIRouter(
    prefix="/api/students",
    tags=["Students"]
)


def serialize_student(student):
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "college": student["college"],
        "department": student["department"],
        "year": student["year"],
        "bio": student.get("bio")
    }


@router.post("/", status_code=201)
def create_student(student: StudentCreate):

    student_data = student.model_dump()

    try:
        result = users_collection.insert_one(student_data)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    created_student = users_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_student(created_student)


@router.get("/{student_id}")
def get_student(student_id: str):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    student = users_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        raise HTTPException(404, "Student not found")

    return serialize_student(student)


@router.put("/{student_id}")
def update_student(student_id: str, student: StudentUpdate):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    update_data = student.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "No update data provided")

    result = users_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Student not found")

    updated_student = users_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    return serialize_student(updated_student)


@router.delete("/{student_id}")
def delete_student(student_id: str):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    result = users_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Student not found")

    return {
        "message": "Student profile deleted successfully"
    }