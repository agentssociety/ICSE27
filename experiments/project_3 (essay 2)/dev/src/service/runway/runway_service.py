from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional
from dataclasses import dataclass

from src.domain.flight.Flight import Flight, FlightStatus, FlightType
from src.domain.runway.Runway import Runway, AlternativeRunway, AircraftType, PermissionLevel
from src.service.flight.flight_service import allocate_slots, SLOT_DURATION_MINUTES, GAP_MINUTES


class Permission:
    def __init__(self, level: PermissionLevel | None = None) -> None:
        self.level = level

    def checkPermission(self, flight_operations: Any, write: Any) -> None:
        pass


class Actor:
    def __init__(self, name: str | None = None, mayPerform: list[Permission] | None = None, role: str | None = None) -> None:
        self.name = name
        self.mayPerform = mayPerform or []
        self.role = role

    def checkAuthentication(self, token: str) -> bool:
        return token is not None and len(token) > 0

    def checkPermission(self, actor: Actor, requiredLevel: PermissionLevel) -> bool:
        return True

    def getPermissions(self) -> list[Permission]:
        return self.mayPerform

    def isOwner(self, actor: Actor) -> bool:
        return self.name == actor.name

    def authenticate(self, credentials: Any) -> Actor:
        return self

    def authenticateUser(self, credentials: Any) -> bool:
        return True

    def returnFalse(self) -> None:
        pass


class AirTrafficControl:
    def __init__(self, permissions: set[Permission] | None = None) -> None:
        self.permissions = permissions or set()


class FlightOperations:
    def __init__(self, permissions: set[Permission] | None = None) -> None:
        self.permissions = permissions or set()


class Passengers:
    def __init__(self, permissions: set[Permission] | None = None) -> None:
        self.permissions = permissions or set()


def get_affected_flights(runway: Runway) -> list[Flight]:
    """Identify all flights scheduled on a closed runway.

    Args:
        runway: The runway that is closed.

    Returns:
        List of flights assigned to this runway.
    """
    return runway.flights


def find_alternative_runways(
    closed_runway: Runway,
    available_runways: list[Runway],
) -> list[Runway]:
    """Find alternative runways that can accommodate flights from a closed runway.

    Args:
        closed_runway: The closed runway.
        available_runways: List of all available runways.

    Returns:
        List of alternative runways that match the closed runway's capabilities.
    """
    alternatives: list[Runway] = []
    for runway in available_runways:
        if runway.runwayId != closed_runway.runwayId and not runway.is_closed():
            # Check if the alternative can handle at least some aircraft types
            if runway.aircraftTypes & closed_runway.aircraftTypes:
                alternatives.append(runway)
    return alternatives


def reassign_flights(
    affected_flights: list[Flight],
    alternative_runways: list[Runway],
) -> dict[str, tuple[Flight, Runway]]:
    """Reassign flights to alternative runways if available.

    Args:
        affected_flights: Flights that need reassignment.
        alternative_runways: Available alternative runways.

    Returns:
        Dictionary mapping flight number -> (flight, assigned runway).
    """
    reassignments: dict[str, tuple[Flight, Runway]] = {}
    if not alternative_runways:
        return reassignments

    runway_index = 0
    for flight in affected_flights:
        # Try to find a suitable runway for this flight's aircraft type
        for _ in range(len(alternative_runways)):
            candidate = alternative_runways[runway_index % len(alternative_runways)]
            runway_index += 1
            if candidate.is_available_for(AircraftType.MEDIUM):
                reassignments[flight.flightNumber] = (flight, candidate)
                break

    return reassignments


def reschedule_flights(
    affected_flights: list[Flight],
    base_time: Optional[datetime] = None,
) -> list[tuple[Flight, datetime, datetime]]:
    """Reschedule flights that cannot be reassigned.

    Args:
        affected_flights: Flights that need rescheduling.
        base_time: Starting time for rescheduling (defaults to now).

    Returns:
        List of (flight, new_start, new_end) tuples.
    """
    if not affected_flights:
        return []

    # Create allocation slots (flight number -> (start, end))
    slots = allocate_slots(affected_flights)

    result: list[tuple[Flight, datetime, datetime]] = []
    for flight in affected_flights:
        if flight.flightNumber in slots:
            start, end = slots[flight.flightNumber]
            result.append((flight, start, end))

    return result


def handle_runway_closure(
    closed_runway: Runway,
    all_runways: list[Runway],
) -> dict:
    """Handle a runway closure by reassigning or rescheduling affected flights.

    Args:
        closed_runway: The runway that is being closed.
        all_runways: All available runways in the system.

    Returns:
        Dictionary with 'reassigned' and 'rescheduled' keys.
    """
    # Step 1: Identify affected flights
    affected = get_affected_flights(closed_runway)

    # Step 2: Find alternative runways
    alternatives = find_alternative_runways(closed_runway, all_runways)

    # Step 3: Reassign to alternatives if available
    reassignments = reassign_flights(affected, alternatives)

    # Step 4: Reschedule remaining
    reassigned_fns = set(reassignments.keys())
    to_reschedule = [f for f in affected if f.flightNumber not in reassigned_fns]
    rescheduled = reschedule_flights(to_reschedule)

    return {
        "affected_count": len(affected),
        "reassigned": reassignments,
        "rescheduled": rescheduled,
        "alternatives_used": len(alternatives),
    }


import uuid
from datetime import datetime, timedelta
from typing import Callable, Optional
from enum import Enum


class SlotStatus(Enum):
    NORMAL = "normal"
    DELAYED = "delayed"
    EMERGENCY = "emergency"
    CANCELLED = "cancelled"


@dataclass
class TimetableEntry:
    """A single entry in the runway slot timetable."""
    slot_id: str
    flight_number: str
    airline: str
    origin: str
    destination: str
    scheduled_time: datetime
    slot_start: datetime
    slot_end: datetime
    runway_id: str
    status: SlotStatus
    delay_minutes: int = 0
    is_emergency: bool = False


class RunwayTimetable:
    """Provides a view of the runway slot timetable."""

    def __init__(
        self,
        get_flights_fn: Callable[[], list[Flight]],
        get_runways_fn: Callable[[], list[Runway]],
        allocate_fn: Callable[[list[Flight]], dict[str, tuple[datetime, datetime]]],
    ):
        self._get_flights = get_flights_fn
        self._get_runways = get_runways_fn
        self._allocate = allocate_fn

    def get_timetable(
        self,
        runway_id: Optional[str] = None,
        time_from: Optional[datetime] = None,
        time_to: Optional[datetime] = None,
    ) -> list[TimetableEntry]:
        """Get the runway slot timetable with optional filtering.

        Args:
            runway_id: Filter by runway ID (None = all runways).
            time_from: Filter slots starting from this time.
            time_to: Filter slots ending at this time.

        Returns:
            List of timetable entries.
        """
        flights = self._get_flights()
        runways = self._get_runways()
        slots = self._allocate(flights)

        # Build runway lookup
        runway_map: dict[str, Runway] = {r.runwayId: r for r in runways}

        entries: list[TimetableEntry] = []
        now = datetime.now()

        for flight in flights:
            if flight.flightNumber not in slots:
                continue

            slot_start, slot_end = slots[flight.flightNumber]

            # Apply filters
            if runway_id is not None:
                # Try to find matching runway
                matched = False
                for rid, rwy in runway_map.items():
                    if rid == runway_id:
                        matched = True
                        break
                if not matched:
                    continue

            if time_from is not None and slot_end < time_from:
                continue
            if time_to is not None and slot_start > time_to:
                continue

            # Determine status
            delay = 0
            if slot_start > flight.scheduledTime:
                delay = int((slot_start - flight.scheduledTime).total_seconds() / 60)

            status = SlotStatus.NORMAL
            if flight.status == FlightStatus.CANCELLED:
                status = SlotStatus.CANCELLED
            elif delay > 0:
                status = SlotStatus.DELAYED

            # Determine which runway this flight is on (from the first runway with flights)
            assigned_runway = runway_id or "unknown"

            entry = TimetableEntry(
                slot_id=str(uuid.uuid4()),
                flight_number=flight.flightNumber,
                airline=flight.airline,
                origin=flight.origin,
                destination=flight.destination,
                scheduled_time=flight.scheduledTime,
                slot_start=slot_start,
                slot_end=slot_end,
                runway_id=assigned_runway,
                status=status,
                delay_minutes=delay,
                is_emergency=False,
            )
            entries.append(entry)

        return entries