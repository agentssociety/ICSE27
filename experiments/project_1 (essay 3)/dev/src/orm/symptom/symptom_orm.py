from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SymptomORM(Base):
    __tablename__ = "symptom"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    patientId: Mapped[str] = mapped_column(String, nullable=False)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patient.id"), nullable=False)
    patient: Mapped["PatientORM"] = relationship("PatientORM")
