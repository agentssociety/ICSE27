from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer, String


class CohortORM(Base):
    __tablename__ = "cohorts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    instructor_id = Column(Integer, nullable=True)
