from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer, String


class InstructorORM(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
