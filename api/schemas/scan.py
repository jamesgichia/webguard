"""
Scan schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class ScanRequest(BaseModel):
    target_url: str
    profile: str = "Standard"


class ScanResponse(BaseModel):
    id: uuid.UUID
    target_url: str
    status: str
    profile: str
    overall_score: float | None = None
    overall_grade: str | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True
