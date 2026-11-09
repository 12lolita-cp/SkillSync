import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


# Secret key used to create and verify JWT tokens
def get_secret_key():
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY environment variable is not set")

    return secret_key

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()


# Hash the password before saving it
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Check whether the entered password matches the stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# Create an access token after successful login
def create_access_token(admin_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": admin_id,
        "role": "admin",
        "exp": expire
    }

    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)

# Verify the access token
def decode_access_token(token: str):
    return jwt.decode(
        token,
        get_secret_key(),
        algorithms=[ALGORITHM]
    )