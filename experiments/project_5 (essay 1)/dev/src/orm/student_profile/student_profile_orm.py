from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer, String, Text


class StudentProfileORM(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, unique=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
