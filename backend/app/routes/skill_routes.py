from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import skills_collection, users_collection
from app.schemas.skill_schema import SkillCreate, SkillUpdate


router = APIRouter(
    prefix="/api/students/{student_id}/skills",
    tags=["Student Skills"]
)


def serialize_skill(skill):
    return {
        "id": str(skill["_id"]),
        "student_id": skill["student_id"],
        "skill_name": skill["skill_name"],
        "category": skill["category"],
        "proficiency": skill["proficiency"],
        "progress": skill["progress"]
    }


def validate_student(student_id):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    student = users_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        raise HTTPException(404, "Student not found")


@router.post("/", status_code=201)
def add_skill(student_id: str, skill: SkillCreate):

    validate_student(student_id)

    skill_data = skill.model_dump()
    skill_data["proficiency"] = skill_data["proficiency"].value
    skill_data["student_id"] = student_id

    result = skills_collection.insert_one(skill_data)

    created_skill = skills_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_skill(created_skill)


@router.get("/")
def get_student_skills(student_id: str):

    validate_student(student_id)

    skills = skills_collection.find(
        {"student_id": student_id}
    )

    return [serialize_skill(skill) for skill in skills]


@router.put("/{skill_id}")
def update_skill(
    student_id: str,
    skill_id: str,
    skill: SkillUpdate
):

    validate_student(student_id)

    if not ObjectId.is_valid(skill_id):
        raise HTTPException(400, "Invalid skill ID")

    update_data = skill.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "No update data provided")

    if "proficiency" in update_data and update_data["proficiency"]:
        update_data["proficiency"] = update_data["proficiency"].value

    result = skills_collection.update_one(
        {
            "_id": ObjectId(skill_id),
            "student_id": student_id
        },
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Skill not found")

    updated_skill = skills_collection.find_one(
        {"_id": ObjectId(skill_id)}
    )

    return serialize_skill(updated_skill)


@router.delete("/{skill_id}")
def delete_skill(student_id: str, skill_id: str):

    validate_student(student_id)

    if not ObjectId.is_valid(skill_id):
        raise HTTPException(400, "Invalid skill ID")

    result = skills_collection.delete_one(
        {
            "_id": ObjectId(skill_id),
            "student_id": student_id
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Skill not found")

    return {
        "message": "Skill deleted successfully"
    }


@router.get("/progress/summary")
def get_skill_progress(student_id: str):

    validate_student(student_id)

    skills = list(
        skills_collection.find(
            {"student_id": student_id}
        )
    )

    if not skills:
        return {
            "total_skills": 0,
            "average_progress": 0
        }

    total_progress = sum(
        skill["progress"] for skill in skills
    )

    average_progress = round(
        total_progress / len(skills), 2
    )

    return {
        "total_skills": len(skills),
        "average_progress": average_progress
    }