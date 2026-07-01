from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class ScheduleORM(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exam_id: Mapped[str] = mapped_column(String, nullable=False)
    open_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    per_attempt_time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
