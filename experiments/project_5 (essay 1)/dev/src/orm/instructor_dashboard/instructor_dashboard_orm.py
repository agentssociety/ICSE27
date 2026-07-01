from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Integer


class InstructorDashboardORM(Base):
    __tablename__ = "instructor_dashboards"
    id = Column(Integer, primary_key=True)
