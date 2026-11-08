from datetime import date

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.database import users_collection, certifications_collection
from app.schemas.certification_schema import (
    CertificationCreate,
    CertificationUpdate
)


router = APIRouter(
    prefix="/api/students/{student_id}/certifications",
    tags=["Student Certifications"]
)


# Convert date strings into Python date objects
def parse_date(value):
    if value is None:
        return None

    if isinstance(value, date):
        return value

    return date.fromisoformat(value)


# Validate whether the student exists
def validate_student(student_id):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid student ID"
        )

    student = users_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


# Calculate certification status
def get_status(expiry_date):
    if expiry_date is None:
        return "No Expiry"

    expiry_date = parse_date(expiry_date)

    if expiry_date < date.today():
        return "Expired"

    return "Active"


# Convert MongoDB certification data into API response
def serialize_certification(certification):
    return {
        "id": str(certification["_id"]),
        "student_id": certification["student_id"],
        "certification_name": certification["certification_name"],
        "issuing_organization": certification["issuing_organization"],
        "issue_date": parse_date(
            certification["issue_date"]
        ).isoformat(),
        "expiry_date": (
            parse_date(certification["expiry_date"]).isoformat()
            if certification.get("expiry_date")
            else None
        ),
        "credential_id": certification.get("credential_id"),
        "credential_url": certification.get("credential_url"),
        "status": get_status(certification.get("expiry_date"))
    }


# ADD CERTIFICATION
@router.post("/", status_code=201)
def add_certification(
    student_id: str,
    certification: CertificationCreate
):
    validate_student(student_id)

    # Validate certification dates
    if (
        certification.expiry_date
        and certification.expiry_date < certification.issue_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Expiry date cannot be before issue date"
        )

    data = certification.model_dump(mode="json")
    data["student_id"] = student_id

    result = certifications_collection.insert_one(data)

    created = certifications_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_certification(created)


# GET ALL CERTIFICATIONS FOR A STUDENT
@router.get("/")
def get_certifications(student_id: str):
    validate_student(student_id)

    certifications = certifications_collection.find(
        {"student_id": student_id}
    )

    return [
        serialize_certification(item)
        for item in certifications
    ]


# UPDATE CERTIFICATION
@router.put("/{certification_id}")
def update_certification(
    student_id: str,
    certification_id: str,
    certification: CertificationUpdate
):
    validate_student(student_id)

    if not ObjectId.is_valid(certification_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid certification ID"
        )

    update_data = certification.model_dump(
        exclude_unset=True,
        mode="json"
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update data provided"
        )

    existing = certifications_collection.find_one({
        "_id": ObjectId(certification_id),
        "student_id": student_id
    })

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    issue_date = parse_date(
        update_data.get("issue_date", existing["issue_date"])
    )

    expiry_date = parse_date(
        update_data.get("expiry_date", existing.get("expiry_date"))
    )

    if expiry_date and expiry_date < issue_date:
        raise HTTPException(
            status_code=400,
            detail="Expiry date cannot be before issue date"
        )

    certifications_collection.update_one(
        {
            "_id": ObjectId(certification_id),
            "student_id": student_id
        },
        {"$set": update_data}
    )

    updated = certifications_collection.find_one(
        {"_id": ObjectId(certification_id)}
    )

    return serialize_certification(updated)


# DELETE CERTIFICATION
@router.delete("/{certification_id}")
def delete_certification(
    student_id: str,
    certification_id: str
):
    validate_student(student_id)

    if not ObjectId.is_valid(certification_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid certification ID"
        )

    result = certifications_collection.delete_one({
        "_id": ObjectId(certification_id),
        "student_id": student_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Certification not found"
        )

    return {
        "message": "Certification deleted successfully"
    }