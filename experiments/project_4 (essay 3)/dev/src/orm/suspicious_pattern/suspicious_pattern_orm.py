from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class SuspiciousPatternORM(Base):
    __tablename__ = "suspicious_pattern"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    withdrawalTransaction_id: Mapped[int] = mapped_column(Integer, nullable=False)
