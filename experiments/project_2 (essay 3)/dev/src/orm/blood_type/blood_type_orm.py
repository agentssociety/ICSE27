from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class BloodTypeORM(Base):
    __tablename__ = "blood_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bloodUnit_id: Mapped[int] = mapped_column(Integer, ForeignKey("blood_unit.id"), nullable=False)
    transfusionRequest_id: Mapped[str] = mapped_column(String, ForeignKey("transfusion_request.id"), nullable=False)
    bloodUnit: Mapped["BloodUnitORM"] = relationship("BloodUnitORM")
    transfusionRequest: Mapped["TransfusionRequestORM"] = relationship("TransfusionRequestORM")
