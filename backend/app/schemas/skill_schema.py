from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProficiencyLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class SkillCreate(BaseModel):
    skill_name: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    proficiency: ProficiencyLevel
    progress: int = Field(default=0, ge=0, le=100)


class SkillUpdate(BaseModel):
    skill_name: Optional[str] = Field(None, min_length=2)
    category: Optional[str] = Field(None, min_length=2)
    proficiency: Optional[ProficiencyLevel] = None
    progress: Optional[int] = Field(None, ge=0, le=100)


class SkillResponse(BaseModel):
    id: str
    student_id: str
    skill_name: str
    category: str
    proficiency: ProficiencyLevel
    progress: int