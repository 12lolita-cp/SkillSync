from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    college: str
    department: str
    year: int = Field(..., ge=1, le=5)
    bio: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    college: Optional[str] = None
    department: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=5)
    bio: Optional[str] = None


class StudentResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    college: str
    department: str
    year: int
    bio: Optional[str] = None