from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Protocol

from src.domain.time_slot.TimeSlot import TimeSlot


class TimeSlotService(Protocol):
    """Protocol for time slot service operations."""

    def create_slot(self, start_time: datetime) -> TimeSlot:
        """Create a new time slot."""
        ...

    def compute_gap(self, end_time1: datetime, start_time2: datetime) -> timedelta:
        """Compute the gap between two time boundaries."""
        ...

    def normalize_to_utc(self, slot: TimeSlot) -> TimeSlot:
        """Normalize a time slot to UTC."""
        ...


class TimeSlotServiceImpl:
    """Implementation of TimeSlotService."""

    def create_slot(self, start_time: datetime) -> TimeSlot:
        """Create a 5-minute time slot starting at the given time."""
        end_time = start_time + timedelta(minutes=5)
        return TimeSlot(startTime=start_time, endTime=end_time)

    def compute_gap(self, end_time1: datetime, start_time2: datetime) -> timedelta:
        """Compute the gap between two time boundaries."""
        return start_time2 - end_time1

    def normalize_to_utc(self, slot: TimeSlot) -> TimeSlot:
        """Return a normalized copy of the slot (naive datetime treated as UTC)."""
        return slot
