from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String, Date, Enum as SqlEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import enum

from src.config.database import Base


class BloodUnitStatusEnum(enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    ISSUED = "issued"
    EXPIRED = "expired"


class BloodUnitORM(Base):
    __tablename__ = "blood_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uniqueID: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    aboType: Mapped[str] = mapped_column(String(2), nullable=False)
    rhFactor: Mapped[str] = mapped_column(String(8), nullable=False)
    collectionDate: Mapped[Date] = mapped_column(Date, nullable=False)
    expiryDate: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[BloodUnitStatusEnum] = mapped_column(SqlEnum(BloodUnitStatusEnum), nullable=False, default=BloodUnitStatusEnum.AVAILABLE)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
