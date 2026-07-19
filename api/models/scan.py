"""
Scan job model.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)  # pending, running, completed, failed
    profile: Mapped[str] = mapped_column(String, default="Standard", nullable=False)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    overall_grade: Mapped[str | None] = mapped_column(String, nullable=True)
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="scans")
    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")
    dimension_scores = relationship("DimensionScoreModel", back_populates="scan", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="scan", uselist=False, cascade="all, delete-orphan")
