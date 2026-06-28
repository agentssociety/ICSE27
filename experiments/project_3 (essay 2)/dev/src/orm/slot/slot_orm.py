from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SlotORM(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flight_id: Mapped[int] = mapped_column(Integer, ForeignKey("flight.id"), nullable=False)
    runway_id: Mapped[int] = mapped_column(Integer, ForeignKey("runway.id"), nullable=False)
    flight: Mapped["FlightORM"] = relationship("FlightORM")
    runway: Mapped["RunwayORM"] = relationship("RunwayORM")
