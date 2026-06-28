from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class SlotORM(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    isAvailable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
