from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class AttemptORM(Base):
    __tablename__ = "attempt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    method_isCompleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
