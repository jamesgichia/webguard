"""
Dimension score model.
"""

import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base


class DimensionScoreModel(Base):
    __tablename__ = "dimension_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scans.id"), nullable=False)
    
    dimension: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    grade: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)

    scan = relationship("Scan", back_populates="dimension_scores")
