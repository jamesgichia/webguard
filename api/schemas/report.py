"""
Report schemas.
"""

import uuid
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: uuid.UUID
    scan_id: uuid.UUID
    has_html: bool
    has_pdf: bool

    class Config:
        from_attributes = True
