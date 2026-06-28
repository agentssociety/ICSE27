from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Pin domain class

Package: orm.pin
Layer: orm
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""

class PinORM(Base):
    __tablename__ = "pins"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    pin_code: Mapped[str] = mapped_column(String(6))
    user_id: Mapped[str] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
