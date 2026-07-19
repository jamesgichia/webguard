"""
Finding model.
"""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, JSON, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)
    
    owasp_id: Mapped[str] = mapped_column(String, nullable=False)
    owasp_name: Mapped[str] = mapped_column(String, nullable=False)
    dimension: Mapped[str] = mapped_column(String, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    business_impact: Mapped[str] = mapped_column(String, nullable=False)
    recommendation: Mapped[str] = mapped_column(String, nullable=False)
    effort: Mapped[str] = mapped_column(String, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)
    references: Mapped[list[str]] = mapped_column(JSON, default=list)

    scan = relationship("Scan", back_populates="findings")
