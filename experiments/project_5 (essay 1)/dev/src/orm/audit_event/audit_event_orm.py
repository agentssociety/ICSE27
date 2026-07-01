from __future__ import annotations

from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from src.config.database import Base


class AuditEventORM(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    instructor_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
