from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SymptomRecordORM(Base):
    __tablename__ = "symptom_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recordId: Mapped[str] = mapped_column(String, nullable=False)
    symptomData: Mapped[str] = mapped_column(String, nullable=False)
    patientId: Mapped[str] = mapped_column(String, nullable=False)
    symptom_id: Mapped[int] = mapped_column(Integer, ForeignKey("symptom.id"), nullable=False)
    symptom: Mapped["SymptomORM"] = relationship("SymptomORM")
