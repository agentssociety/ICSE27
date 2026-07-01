from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Boolean, Column, Float, Integer, String


class CompetencyBreakdownORM(Base):
    __tablename__ = "competency_breakdowns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_session_id = Column(Integer, nullable=False)
    competency_name = Column(String, nullable=False)
    score = Column(Float, nullable=False, default=0.0)
    max_score = Column(Float, nullable=False, default=0.0)
    is_weak = Column(Boolean, nullable=False, default=False)
