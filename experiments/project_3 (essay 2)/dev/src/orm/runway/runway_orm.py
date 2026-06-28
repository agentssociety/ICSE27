from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class RunwayORM(Base):
    __tablename__ = "runway"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    runwayId: Mapped[str] = mapped_column(String, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False, default=3000)
    timeSlot: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
