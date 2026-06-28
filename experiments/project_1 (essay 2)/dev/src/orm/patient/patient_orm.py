from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base

class PatientORM(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symptoms: Mapped[str] = mapped_column(String, nullable=False)
    urgencyLevel: Mapped[int] = mapped_column(Integer, nullable=False)
    queuePosition: Mapped[int] = mapped_column(Integer, nullable=False)
    arrivalTime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    urgency: Mapped[str] = mapped_column(String, nullable=False)