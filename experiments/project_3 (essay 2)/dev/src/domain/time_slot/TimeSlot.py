from __future__ import annotations

from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.flight import Flight

"""
Domain layer for the TimeSlot domain class

Package: domain.time_slot
Layer: domain
Related tasks: None
"""

DateTime = datetime
Duration = timedelta


@dataclass
class TimeSlotId:
    value: str = ""

    def __post_init__(self) -> None:
        if not self.value:
            import uuid
            self.value = str(uuid.uuid4())


@dataclass
class TimeSlotCreatedEvent:
    slot: "TimeSlot"


@dataclass
class TimeSlotUpdatedEvent:
    slot: "TimeSlot"


@dataclass
class TimeSlot:
    startTime: DateTime
    endTime: DateTime
    flight: Optional[Any] = None

    def __post_init__(self) -> None:
        self.duration: Duration = self.endTime - self.startTime
        self.start: DateTime = self.startTime
        self.end: DateTime = self.endTime

    def createSlot(self, startTime: DateTime) -> "TimeSlot":
        """Create a 5-minute time slot starting at the given time."""
        end_time = startTime + timedelta(minutes=5)
        return TimeSlot(startTime=startTime, endTime=end_time)

    def computeGap(self, endTime1: DateTime, startTime2: DateTime) -> Duration:
        """Compute the gap between two time boundaries."""
        return startTime2 - endTime1

    def normalizeToUTC(self, slot: "TimeSlot") -> "TimeSlot":
        """Return a normalized copy of the slot (naive datetime treated as UTC)."""
        return slot
