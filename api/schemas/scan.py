"""
Scan schemas.
"""

import uuid
from datetime import datetime
from typing import Any

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


class FindingResponse(BaseModel):
    id: uuid.UUID
    owasp_id: str
    owasp_name: str
    dimension: str
    passed: bool
    severity: str
    title: str
    description: str
    business_impact: str
    recommendation: str
    effort: str
    evidence: dict[str, Any] = {}
    references: list[str] = []

    class Config:
        from_attributes = True


class DimensionScoreResponse(BaseModel):
    id: uuid.UUID
    dimension: str
    score: float
    weight: float
    grade: str
    label: str

    class Config:
        from_attributes = True


class ScanDetailResponse(ScanResponse):
    """Extended scan response including findings and dimension scores."""
    findings: list[FindingResponse] = []
    dimension_scores: list[DimensionScoreResponse] = []
