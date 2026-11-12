
from datetime import date

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from app.database import (
    applications_collection,
    users_collection,
    internships_collection
)

from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationStatusUpdate
)

from app.routes.auth_routes import get_current_admin


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"]
)


def serialize_application(application):
    return {
        "id": str(application["_id"]),
        "student_id": str(application["student_id"]),
        "internship_id": str(application["internship_id"]),
        "cover_letter": application.get("cover_letter"),
        "status": application["status"],
        "applied_on": application["applied_on"]
    }


# Student submits an application
@router.post("/", status_code=201)
def create_application(application: ApplicationCreate):

    if not ObjectId.is_valid(application.student_id):
        raise HTTPException(400, "Invalid student ID")

    if not ObjectId.is_valid(application.internship_id):
        raise HTTPException(400, "Invalid internship ID")

    student = users_collection.find_one({
        "_id": ObjectId(application.student_id)
    })

    if not student:
        raise HTTPException(404, "Student not found")

    internship = internships_collection.find_one({
        "_id": ObjectId(application.internship_id)
    })

    if not internship:
        raise HTTPException(404, "Internship not found")

    if internship["status"] != "Active":
        raise HTTPException(400, "This internship is not active")

    deadline = date.fromisoformat(
        internship["application_deadline"]
    )

    if deadline < date.today():
        raise HTTPException(400, "Application deadline has passed")

    existing_application = applications_collection.find_one({
        "student_id": application.student_id,
        "internship_id": application.internship_id
    })

    if existing_application:
        raise HTTPException(
            409,
            "You have already applied for this internship"
        )

    application_data = {
        "student_id": application.student_id,
        "internship_id": application.internship_id,
        "cover_letter": application.cover_letter,
        "status": "Applied",
        "applied_on": date.today().isoformat()
    }

    result = applications_collection.insert_one(application_data)

    created_application = applications_collection.find_one({
        "_id": result.inserted_id
    })

    return serialize_application(created_application)


# Student views applications associated with a student ID
@router.get("/student/{student_id}")
def get_student_applications(student_id: str):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    student = users_collection.find_one({
        "_id": ObjectId(student_id)
    })

    if not student:
        raise HTTPException(404, "Student not found")

    applications = applications_collection.find({
        "student_id": student_id
    })

    return [
        serialize_application(application)
        for application in applications
    ]


# Admin views all applications
@router.get("/")
def get_all_applications(
    current_admin: dict = Depends(get_current_admin)
):

    applications = applications_collection.find()

    return [
        serialize_application(application)
        for application in applications
    ]


# Admin updates an application status
@router.put("/{application_id}/status")
def update_application_status(
    application_id: str,
    application: ApplicationStatusUpdate,
    current_admin: dict = Depends(get_current_admin)
):

    if not ObjectId.is_valid(application_id):
        raise HTTPException(400, "Invalid application ID")

    result = applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": application.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Application not found")

    updated_application = applications_collection.find_one({
        "_id": ObjectId(application_id)
    })

    return serialize_application(updated_application)
