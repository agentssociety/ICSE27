from __future__ import annotations

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BloodUnitORM(Base):
    __tablename__ = "blood_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bloodType: Mapped[str] = mapped_column(String, nullable=False)
    rhFactor: Mapped[str] = mapped_column(String, nullable=False)
    donationDate: Mapped[str] = mapped_column(String, nullable=False)
    expirationDate: Mapped[str] = mapped_column(String, nullable=True)
    isExpiring: Mapped[bool] = mapped_column(Boolean, default=False)
