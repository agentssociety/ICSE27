from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class TimeSlotORM(Base):
    __tablename__ = "time_slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flight_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("flight.id"), nullable=True)
    flight: Mapped[Optional["FlightORM"]] = relationship("FlightORM")
