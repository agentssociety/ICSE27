from __future__ import annotations

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Card domain class

Package: orm.card
Layer: orm
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""

class CardORM(Base):
    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36))
    card_number: Mapped[str] = mapped_column(String(20), unique=True)
