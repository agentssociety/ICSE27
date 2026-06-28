from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Interval, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SlotORM(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    startTime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    endTime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[str] = mapped_column(String, nullable=False)  # ISO timedelta
    gapAfter: Mapped[str] = mapped_column(String, nullable=False)  # ISO timedelta
"""
Orm layer for the Slot domain class

Package: orm.slot
Layer: orm
Related tasks: #73, #74, #75, #76, #77, #78
Requirement coverage:
- Allocate 5-minute slots with a 3-minute gap between successive slots
- Prioritize Arrivals Over Departures When Allocating Slots
- Detect and Prevent Slot Overlaps
- Runway Closure and Flight Reassignment Management
- Prioritize Emergency Flights and Re-queue Non-Emergency Flights
"""