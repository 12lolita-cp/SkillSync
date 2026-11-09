
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class InternshipCreate(BaseModel):
    title: str = Field(..., min_length=2)
    company: str = Field(..., min_length=2)
    description: str = Field(..., min_length=10)
    location: str
    skills_required: list[str] = Field(default_factory=list)
    duration: str
    stipend: Optional[float] = Field(None, ge=0)
    application_deadline: date
    status: Literal["Active", "Inactive"] = "Active"


class InternshipUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    company: Optional[str] = Field(None, min_length=2)
    description: Optional[str] = Field(None, min_length=10)
    location: Optional[str] = None
    skills_required: Optional[list[str]] = None
    duration: Optional[str] = None
    stipend: Optional[float] = Field(None, ge=0)
    application_deadline: Optional[date] = None
    status: Optional[Literal["Active", "Inactive"]] = None
