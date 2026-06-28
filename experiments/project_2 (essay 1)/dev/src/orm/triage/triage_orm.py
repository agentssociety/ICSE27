from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.orm.base import Base


class TriageAssessmentORM(Base):
    __tablename__ = "triage_assessment"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    patientId: Mapped[str] = mapped_column(String, nullable=False, index=True)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    createdAt: Mapped[str] = mapped_column(String, nullable=False)
    inQueue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
