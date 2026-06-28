from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from src.config.database import Base


class ReservationStatusEnum(enum.Enum):
    ACTIVE = "active"
    RELEASED = "released"
    ISSUED = "issued"


class ReservationORM(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bloodUnitId: Mapped[str] = mapped_column(String, nullable=False)
    transfusionRequestId: Mapped[str] = mapped_column(String, nullable=False)
    bloodUnit_id: Mapped[int] = mapped_column(Integer, ForeignKey("blood_unit.id"), nullable=False)
    reservationTimestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expiryTimestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ReservationStatusEnum] = mapped_column(SqlEnum(ReservationStatusEnum), nullable=False, default=ReservationStatusEnum.ACTIVE)
    bloodUnit: Mapped["BloodUnitORM"] = relationship("BloodUnitORM")
