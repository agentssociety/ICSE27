from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class EmergencyFlightORM(Base):
    __tablename__ = "emergency_flight"

    id: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    flight_id: Mapped[int] = mapped_column(Integer, ForeignKey("flight.id"), nullable=False)
    slot_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("slot.id"), nullable=True)
    flight: Mapped["FlightORM"] = relationship("FlightORM")
    slot: Mapped[Optional["SlotORM"]] = relationship("SlotORM")
