"""Data models for the flight scheduling system.

This module defines the core data structures: Flight, Slot, and Runway.
These classes are used by the Scheduler to manage flight operations.
"""

from __future__ import annotations

import datetime
from typing import Dict, List, Optional


class Flight:
    """Represents a flight requesting takeoff or landing."""

    def __init__(
        self,
        flight_id: str,
        flight_type: str,  # 'arrival' or 'departure'
        estimated_time: datetime.datetime,
        is_emergency: bool = False,
    ) -> None:
        """Initialize a flight.

        Args:
            flight_id: Unique identifier for the flight.
            flight_type: Either 'arrival' or 'departure'.
            estimated_time: Scheduled time for the flight.
            is_emergency: Whether this flight has emergency status.
        """
        self.flight_id = flight_id
        self.flight_type = flight_type
        self.estimated_time = estimated_time
        self.is_emergency = is_emergency
        self.is_delayed = False
        self.assigned_slot: Optional[Slot] = None

    def mark_delayed(self) -> None:
        """Mark this flight as delayed."""
        self.is_delayed = True

    def __lt__(self, other: Flight) -> bool:
        """Compare flights for priority queue ordering.

        Priority order:
        1. Emergency flights first.
        2. Arrivals before departures.
        3. Earlier estimated time first.

        Args:
            other: Another flight to compare against.

        Returns:
            True if this flight has higher priority.
        """
        if self.is_emergency != other.is_emergency:
            return self.is_emergency > other.is_emergency
        if self.flight_type != other.flight_type:
            return self.flight_type == "arrival"
        return self.estimated_time < other.estimated_time

    def __repr__(self) -> str:
        return (
            f"Flight({self.flight_id}, {self.flight_type}, "
            f"{self.estimated_time}, emergency={self.is_emergency})"
        )


class Slot:
    """A time slot on a runway for a flight."""

    SLOT_DURATION_MINUTES = 5

    def __init__(self, runway: int, start_time: datetime.datetime) -> None:
        """Initialize a slot.

        Args:
            runway: Runway number (1 or 2).
            start_time: Start time of the slot.
        """
        self.runway = runway
        self.start_time = start_time
        self.end_time = start_time + datetime.timedelta(
            minutes=self.SLOT_DURATION_MINUTES
        )
        self.flight: Optional[Flight] = None

    def is_available(self) -> bool:
        """Check if this slot is not occupied by a flight.

        Returns:
            True if the slot is free.
        """
        return self.flight is None

    def assign_flight(self, flight: Flight) -> None:
        """Assign a flight to this slot.

        Args:
            flight: The flight to assign.
        """
        self.flight = flight
        flight.assigned_slot = self

    def release(self) -> None:
        """Release the slot, removing any assigned flight."""
        if self.flight is not None:
            self.flight.assigned_slot = None
            self.flight = None

    def __repr__(self) -> str:
        status = "free" if self.flight is None else f"flight={self.flight.flight_id}"
        return (
            f"Slot(runway={self.runway}, {self.start_time}-{self.end_time}, {status})"
        )


class Runway:
    """Represents a single airport runway with a schedule of slots."""

    def __init__(self, runway_id: int) -> None:
        """Initialize a runway.

        Args:
            runway_id: Unique runway identifier (1 or 2).
        """
        self.runway_id = runway_id
        self.is_open = True
        self.slots: List[Slot] = []
        self.schedule: Dict[datetime.datetime, Slot] = {}

    def close(self) -> None:
        """Close this runway."""
        self.is_open = False

    def open(self) -> None:
        """Open this runway."""
        self.is_open = True

    def get_next_available_slot(
        self, after_time: datetime.datetime
    ) -> Optional[Slot]:
        """Find the earliest available slot after the given time.

        Slots are created on demand if none exist. This method generates
        a slot at the next round 5-minute boundary if none exists.

        Args:
            after_time: The earliest acceptable start time.

        Returns:
            The first available Slot, or None if runway is closed.
        """
        if not self.is_open:
            return None
        # Round up to the next 5-minute boundary
        start_minute = (after_time.minute // 5) * 5
        if start_minute < after_time.minute:
            start_minute += 5
        slot_start = after_time.replace(
            minute=start_minute, second=0, microsecond=0
        )
        # Check if a slot already exists at this time
        existing_slot = self.schedule.get(slot_start)
        if existing_slot is not None:
            if existing_slot.is_available():
                return existing_slot
            # Otherwise move to next boundary
            slot_start += datetime.timedelta(minutes=5)
        # Create a new slot if needed
        slot = Slot(self.runway_id, slot_start)
        self.slots.append(slot)
        self.schedule[slot_start] = slot
        return slot

    def get_slots_in_range(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> List[Slot]:
        """Retrieve all slots that overlap with the given time range.

        Args:
            start: Start of the range.
            end: End of the range.

        Returns:
            List of slots in the range, sorted by start time.
        """
        sorted_slots = sorted(self.slots, key=lambda s: s.start_time)
        return [s for s in sorted_slots if s.start_time >= start and s.end_time <= end]

    def __repr__(self) -> str:
        status = "open" if self.is_open else "closed"
        return f"Runway {self.runway_id} ({status}, {len(self.slots)} slots)"
