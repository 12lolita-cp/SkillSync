
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ApplicationCreate(BaseModel):
    student_id: str
    internship_id: str
    cover_letter: Optional[str] = Field(
        None,
        max_length=2000
    )


class ApplicationStatusUpdate(BaseModel):
    status: Literal[
        "Applied",
        "Under Review",
        "Shortlisted",
        "Rejected",
        "Selected"
    ]
