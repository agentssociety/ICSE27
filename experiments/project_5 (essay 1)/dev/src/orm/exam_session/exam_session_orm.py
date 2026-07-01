from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class ExamSessionORM(Base):
    __tablename__ = "exam_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exam_id: Mapped[int] = mapped_column(Integer, nullable=False)
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
