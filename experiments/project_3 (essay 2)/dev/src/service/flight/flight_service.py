from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Protocol

from src.domain.flight.Flight import Flight, FlightType, FlightStatus


SLOT_DURATION_MINUTES = 5
GAP_MINUTES = 3


def allocate_slots(flights: list[Flight]) -> dict[str, tuple[datetime, datetime]]:
    """Allocate 5-minute time slots to flights with 3-minute gaps.

    Args:
        flights: List of flights sorted by scheduled time.

    Returns:
        Dictionary mapping flight number -> (slot_start, slot_end).
    """
    if not flights:
        return {}

    # Sort flights by scheduled time, arrivals before departures
    sorted_flights = sorted(
        flights,
        key=lambda f: (
            f.scheduledTime,
            0 if f.type == FlightType.ARRIVAL else 1,
        ),
    )

    result: dict[str, tuple[datetime, datetime]] = {}
    current_time: Optional[datetime] = None

    for flight in sorted_flights:
        if current_time is None:
            # First slot starts at the flight's scheduled time
            slot_start = flight.scheduledTime
        else:
            # Next slot starts after the gap from the previous slot end
            candidate_start = current_time + timedelta(minutes=GAP_MINUTES)
            slot_start = max(candidate_start, flight.scheduledTime)

        slot_end = slot_start + timedelta(minutes=SLOT_DURATION_MINUTES)
        result[flight.flightNumber] = (slot_start, slot_end)
        current_time = slot_end

    return result


class FlightService(Protocol):
    """Protocol for flight service operations."""

    def register_flight(self, flight: Flight) -> Flight:
        """Register a new flight."""
        ...

    def cancel_flight(self, flight_number: str) -> bool:
        """Cancel a flight."""
        ...

    def update_schedule(self, flight_number: str, new_time: datetime) -> bool:
        """Update a flight's scheduled time."""
        ...

    def get_all_flights(self) -> list[Flight]:
        """Get all registered flights."""
        ...

    def allocate_time_slots(self) -> dict[str, tuple[datetime, datetime]]:
        """Allocate time slots to all active flights."""
        ...

    def get_flight_slot(self, flight_number: str) -> Optional[tuple[datetime, datetime]]:
        """Get the allocated time slot for a specific flight."""
        ...


def detect_overlapping_slots(slots: dict[str, tuple[datetime, datetime]]) -> list[str]:
    """Detect overlapping time slots among flights.

    Args:
        slots: Mapping of flight number -> (slot_start, slot_end).

    Returns:
        List of flight numbers that have overlapping slots.
    """
    overlapping: list[str] = []
    sorted_flights = sorted(slots.items(), key=lambda x: x[1][0])

    for i in range(len(sorted_flights) - 1):
        fn1, (_, end1) = sorted_flights[i]
        fn2, (start2, _) = sorted_flights[i + 1]

        if start2 < end1:
            overlapping.append(fn1)
            overlapping.append(fn2)

    # Remove duplicates while preserving order
    seen: set[str] = set()
    unique_overlapping: list[str] = []
    for fn in overlapping:
        if fn not in seen:
            seen.add(fn)
            unique_overlapping.append(fn)

    return unique_overlapping


def detect_gap_violations(slots: dict[str, tuple[datetime, datetime]]) -> list[tuple[str, str, float]]:
    """Detect slots where the gap between them is less than 3 minutes.

    Args:
        slots: Mapping of flight number -> (slot_start, slot_end).

    Returns:
        List of (flight1, flight2, actual_gap_minutes) for violations.
    """
    violations: list[tuple[str, str, float]] = []
    sorted_flights = sorted(slots.items(), key=lambda x: x[1][0])

    for i in range(len(sorted_flights) - 1):
        fn1, (_, end1) = sorted_flights[i]
        fn2, (start2, _) = sorted_flights[i + 1]

        gap_minutes = (start2 - end1).total_seconds() / 60.0
        if gap_minutes < GAP_MINUTES:
            violations.append((fn1, fn2, gap_minutes))

    return violations


def handle_emergency(
    emergency_flight: Flight,
    all_flights: list[Flight],
    current_slots: dict[str, tuple[datetime, datetime]] | None = None,
) -> dict[str, tuple[datetime, datetime]]:
    """Assign an immediate priority slot to an emergency flight.

    Args:
        emergency_flight: The flight needing emergency priority.
        all_flights: All currently scheduled flights.
        current_slots: Current slot assignments (if any).

    Returns:
        Updated slot assignments with the emergency flight prioritized.
    """
    from datetime import datetime, timedelta

    # Create a list of all flights including the emergency one
    emergency_list = [emergency_flight]
    other_flights = [f for f in all_flights if f.flightNumber != emergency_flight.flightNumber]

    # Emergency flight gets the earliest possible slot
    now = datetime.now()
    emergency_slot_start = now
    emergency_slot_end = emergency_slot_start + timedelta(minutes=SLOT_DURATION_MINUTES)

    # Recursively allocate slots for remaining flights after emergency
    updated_slots: dict[str, tuple[datetime, datetime]] = {}
    updated_slots[emergency_flight.flightNumber] = (emergency_slot_start, emergency_slot_end)

    # Reschedule other flights after emergency slot + gap
    current_time = emergency_slot_end
    for flight in sorted(other_flights, key=lambda f: f.scheduledTime):
        slot_start = max(current_time + timedelta(minutes=GAP_MINUTES), flight.scheduledTime)
        slot_end = slot_start + timedelta(minutes=SLOT_DURATION_MINUTES)
        updated_slots[flight.flightNumber] = (slot_start, slot_end)
        current_time = slot_end

    return updated_slots