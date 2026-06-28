from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.orm.base import Base


class PatientORM(Base):
    __tablename__ = "patient"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    firstName: Mapped[str] = mapped_column(String, nullable=False)
    lastName: Mapped[str] = mapped_column(String, nullable=False)
    dateOfBirth: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    contactPhone: Mapped[str] = mapped_column(String, nullable=False)
    contactEmail: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
