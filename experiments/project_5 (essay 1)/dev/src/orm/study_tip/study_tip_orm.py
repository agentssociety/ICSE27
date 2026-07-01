from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer, String, Text


class StudyTipORM(Base):
    __tablename__ = "study_tips"
    id = Column(Integer, primary_key=True, autoincrement=True)
    competency_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
