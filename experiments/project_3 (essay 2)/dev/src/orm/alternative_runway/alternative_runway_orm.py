from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AlternativeRunwayORM(Base):
    __tablename__ = "alternative_runway"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    isAvailable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    runway_id: Mapped[int] = mapped_column(Integer, ForeignKey("runway.id"), nullable=False)
    runway: Mapped["RunwayORM"] = relationship("RunwayORM")
