from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CertificationCreate(BaseModel):
    certification_name: str = Field(..., min_length=2)
    issuing_organization: str = Field(..., min_length=2)
    issue_date: date
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None


class CertificationUpdate(BaseModel):
    certification_name: Optional[str] = Field(None, min_length=2)
    issuing_organization: Optional[str] = Field(None, min_length=2)
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None