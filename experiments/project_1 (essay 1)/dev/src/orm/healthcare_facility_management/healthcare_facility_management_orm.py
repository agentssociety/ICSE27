from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class HealthcareFacilityManagementORM(Base):
    __tablename__ = "healthcare_facility_management"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
