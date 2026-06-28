from __future__ import annotations

from datetime import date
from typing import Optional
from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class BloodUnitORM(Base):
    __tablename__ = "blood_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    abo_rh_type: Mapped[str] = mapped_column(String, nullable=False)
    collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_expired: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
