
import os
import secrets
import jwt

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import admins_collection
from app.schemas.auth_schema import AdminCreate, AdminLogin, TokenResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# Admin registration (one-time setup)
@router.post("/admin/register", status_code=201)
def register_admin(
    admin: AdminCreate,
    setup_key: str = Header(..., alias="X-Admin-Setup-Key")
):
    expected_key = os.getenv("ADMIN_SETUP_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=503,
            detail="Admin registration is not configured"
        )

    if not secrets.compare_digest(setup_key, expected_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid admin setup key"
        )

    # Allow registration only if no admin exists
    if admins_collection.count_documents({}) > 0:
        raise HTTPException(
            status_code=403,
            detail="Admin registration is already completed"
        )

    admin_data = {
        "name": admin.name,
        "email": admin.email,
        "hashed_password": hash_password(admin.password),
        "role": "admin"
    }

    try:
        result = admins_collection.insert_one(admin_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Admin email already registered"
        )

    return {
        "message": "Admin registered successfully",
        "admin_id": str(result.inserted_id)
    }


# Admin login
@router.post("/admin/login", response_model=TokenResponse)
def login_admin(admin: AdminLogin):
    existing_admin = admins_collection.find_one(
        {"email": admin.email}
    )

    if not existing_admin or not verify_password(
        admin.password,
        existing_admin["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(str(existing_admin["_id"]))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Verify that the logged-in user is an admin
security = HTTPBearer()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    admin_id = payload.get("sub")

    if not admin_id or not ObjectId.is_valid(admin_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid admin token"
        )

    admin = admins_collection.find_one(
        {"_id": ObjectId(admin_id)}
    )

    if not admin or admin.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"],
        "role": admin["role"]
    }
