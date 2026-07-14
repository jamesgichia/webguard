"""
Report model.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)
    
    html_report_path: Mapped[str | None] = mapped_column(String, nullable=True)
    pdf_report_path: Mapped[str | None] = mapped_column(String, nullable=True)
    json_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    scan = relationship("Scan", back_populates="report")
