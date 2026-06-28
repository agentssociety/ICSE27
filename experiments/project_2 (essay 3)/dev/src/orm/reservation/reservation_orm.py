from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class ReservationORM(Base):
    __tablename__ = "reservation"

    id: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    request_id: Mapped[str] = mapped_column(String, ForeignKey("transfusion_request.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, ForeignKey("blood_unit.id"), nullable=False)
    request: Mapped["TransfusionRequestORM"] = relationship("TransfusionRequestORM")
    unit: Mapped["BloodUnitORM"] = relationship("BloodUnitORM")
