
from fastapi import APIRouter, HTTPException, Query, Depends
from bson import ObjectId

from app.database import internships_collection
from app.schemas.internship_schema import (
    InternshipCreate,
    InternshipUpdate
)
from app.routes.auth_routes import get_current_admin

router = APIRouter(
    prefix="/api/internships",
    tags=["Internships"]
)


def serialize_internship(internship):
    return {
        "id": str(internship["_id"]),
        "title": internship["title"],
        "company": internship["company"],
        "description": internship["description"],
        "location": internship["location"],
        "skills_required": internship["skills_required"],
        "duration": internship["duration"],
        "stipend": internship.get("stipend"),
        "application_deadline": str(internship["application_deadline"]),
        "status": internship["status"]
    }


# 1. Create an internship
@router.post("/", status_code=201)
def create_internship(
    internship: InternshipCreate,
    current_admin: dict = Depends(get_current_admin)
):
    internship_data = internship.model_dump()
    internship_data["application_deadline"] = internship.application_deadline.isoformat()

    result = internships_collection.insert_one(internship_data)

    created_internship = internships_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_internship(created_internship)


# 2. View all active internships with search and filters
@router.get("/")
def get_internships(
    search: str = Query(default=""),
    location: str = Query(default=""),
    skill: str = Query(default=""),
    internship_status: str = Query(default="Active")
):
    filters = {}

    if internship_status:
        filters["status"] = internship_status

    if location:
        filters["location"] = {
            "$regex": location,
            "$options": "i"
        }

    if skill:
        filters["skills_required"] = {
            "$regex": skill,
            "$options": "i"
        }

    if search:
        filters["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"company": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    internships = internships_collection.find(filters)

    return [
        serialize_internship(internship)
        for internship in internships
    ]


# 3. View internship details
@router.get("/{internship_id}")
def get_internship(internship_id: str):
    if not ObjectId.is_valid(internship_id):
        raise HTTPException(400, "Invalid internship ID")

    internship = internships_collection.find_one(
        {"_id": ObjectId(internship_id)}
    )

    if not internship:
        raise HTTPException(404, "Internship not found")

    return serialize_internship(internship)


# 4. Update an internship
@router.put("/{internship_id}")
def update_internship(
    internship_id: str,
    internship: InternshipUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    if not ObjectId.is_valid(internship_id):
        raise HTTPException(400, "Invalid internship ID")

    update_data = internship.model_dump(exclude_unset=True)
    if "application_deadline" in update_data and update_data["application_deadline"]:
        update_data["application_deadline"] = update_data["application_deadline"].isoformat()
    if not update_data:
        raise HTTPException(400, "No update data provided")

    result = internships_collection.update_one(
        {"_id": ObjectId(internship_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Internship not found")

    updated_internship = internships_collection.find_one(
        {"_id": ObjectId(internship_id)}
    )

    return serialize_internship(updated_internship)


# 5. Delete an internship
@router.delete("/{internship_id}")
def delete_internship(
    internship_id: str,
    current_admin: dict = Depends(get_current_admin)
    ):
    if not ObjectId.is_valid(internship_id):
        raise HTTPException(400, "Invalid internship ID")

    result = internships_collection.delete_one(
        {"_id": ObjectId(internship_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Internship not found")

    return {"message": "Internship deleted successfully"}
