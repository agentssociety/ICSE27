from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class CohortLeaderboardORM(Base):
    __tablename__ = "cohort_leaderboard"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
