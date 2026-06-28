from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class PatientRecordORM(Base):
    __tablename__ = "patient_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("triage_nurse.id"), nullable=False)
    owner: Mapped["TriageNurseORM"] = relationship("TriageNurseORM")
