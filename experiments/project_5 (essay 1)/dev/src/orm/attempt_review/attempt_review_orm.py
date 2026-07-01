from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class AttemptReviewORM(Base):
    __tablename__ = "attempt_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    competency_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    question_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
