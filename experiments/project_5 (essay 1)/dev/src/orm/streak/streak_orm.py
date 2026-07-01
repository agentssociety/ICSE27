from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer


class StreakORM(Base):
    __tablename__ = "streaks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
