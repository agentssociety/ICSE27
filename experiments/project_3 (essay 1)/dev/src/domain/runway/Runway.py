from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.flight import Flight
    from src.domain.slot import Slot

"""
Domain layer for the Runway domain class

Package: domain.runway
Layer: domain
Related tasks: #50, #52
Requirement coverage:
- Automatic Reassignment of Flights During Runway Closure
- View Runway Slot Timetable
"""

class RunwayStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"

class WakeTurbulenceCategory(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SUPER = "super"

class PermissionLevel(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class PreState(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    PRE3 = "pre3"
    PRE4 = "pre4"

class PostState(Enum):
    POST1 = "post1"
    POST2 = "post2"


@dataclass
class Runway:
    id: str
    status: RunwayStatus
    capacity: int
    configuration: str
    aircraftTypeCompatibility: list[str]
    flights: list[Flight] = field(default_factory=list)
    slot: Optional[Slot] = None

    def findAlternativeRunways(self, aircraftType: Any, requiredCapacity: Any) -> list["Runway"]:
        """Find alternative runways that match the given aircraft type and capacity requirements.
        Returns a list of compatible runways."""
        compatible = []
        if self.status == RunwayStatus.OPEN and self.capacity >= requiredCapacity:
            if self.checkCompatibility(aircraftType, self):
                compatible.append(self)
        return compatible

    def filterByConfiguration(self, aircraftType: Any) -> bool:
        """Check if this runway's configuration is compatible with the given aircraft type."""
        if not self.aircraftTypeCompatibility:
            return True  # No restrictions means compatible by default
        aircraft_type_str = str(aircraftType) if not hasattr(aircraftType, '__iter__') else str(aircraftType)
        return aircraft_type_str in self.aircraftTypeCompatibility or any(
            comp.lower() in aircraft_type_str.lower() for comp in self.aircraftTypeCompatibility
        )

    def filterByStatus(self, OPEN: Any) -> bool:
        """Check if runway status matches the given status."""
        return self.status == OPEN

    def checkCompatibility(self, flight: Any, alternativeRunway: Any) -> bool:
        """Check if a flight is compatible with an alternative runway."""
        if isinstance(flight, str):
            aircraft_type = flight
        elif hasattr(flight, 'aircraftType'):
            aircraft_type = flight.aircraftType
        else:
            aircraft_type = str(flight)

        runway_obj = alternativeRunway if isinstance(alternativeRunway, Runway) else self
        return runway_obj.filterByConfiguration(aircraft_type)


@dataclass
class Aircraft:
    type: str
    size: str
    wakeTurbulenceCategory: WakeTurbulenceCategory

    def getAircraft(self, flight_aircraftType: Any) -> "Aircraft":
        """Retrieve aircraft matching the given type from flight data."""
        aircraft_type_str = flight_aircraftType if isinstance(flight_aircraftType, str) else str(flight_aircraftType)
        return Aircraft(
            type=aircraft_type_str,
            size="medium",  # Default size for matched aircraft
            wakeTurbulenceCategory=WakeTurbulenceCategory.MEDIUM,
        )

    def isCompatible(self, aircraftType: Any, configuration: Any) -> bool:
        """Check if the aircraft type is compatible with a given runway configuration."""
        config_str = configuration if isinstance(configuration, str) else str(configuration)
        type_str = aircraftType if isinstance(aircraftType, str) else str(aircraftType)
        # Basic compatibility: aircraft type should match configuration somehow
        return type_str.lower() in config_str.lower() or config_str.lower() in type_str.lower()


@dataclass
class TrafficData:
    currentRunwayAssignments: list[Slot]
    queuedFlights: list[Flight]
    runwayLoads: dict["Runway", int]

    def updateCurrentAssignments(self, flight: Any, runway: Any) -> None:
        """Update the current runway assignments with a new flight assignment."""
        if hasattr(flight, 'slot') and flight.slot is not None:
            self.currentRunwayAssignments.append(flight.slot)
        # Update runway load
        runway_key = runway if isinstance(runway, Runway) else None
        if runway_key and runway_key in self.runwayLoads:
            self.runwayLoads[runway_key] += 1
        elif runway_key:
            self.runwayLoads[runway_key] = 1


@dataclass
class SeparationRule:
    wakeTurbulenceSeparation: dict[tuple[WakeTurbulenceCategory, WakeTurbulenceCategory], int]
    minimumRunwaySeparationTime: int

    def validateSeparation(self, flight: Any, proposedSlot: Any, runway: Any, existingSlots: Any) -> bool:
        """Validate that a proposed slot maintains proper separation from existing slots."""
        if not existingSlots:
            return True
        # Check time separation from existing slots
        proposed_time = proposedSlot.time if hasattr(proposedSlot, 'time') else int(proposedSlot)
        for slot in existingSlots:
            existing_time = slot.time if hasattr(slot, 'time') else int(slot)
            if abs(proposed_time - existing_time) < self.minimumRunwaySeparationTime:
                return False
        return True

    def verifyAllAssignments(self) -> bool:
        """Verify that all existing assignments maintain proper separation."""
        return True  # Override in concrete implementations


@dataclass
class Resource:
    owner: str

    def checkAccess(self, resource_Runway: Any, actor_System: Any) -> bool:
        """Check if an actor has access to the resource."""
        return True  # Default implementation allows access


@dataclass
class Permission:
    level: PermissionLevel

    def getPermission(self, actor: Any, resource: Any) -> PermissionLevel:
        """Get the permission level for a given actor on a resource."""
        return self.level


@dataclass
class State:
    preconditionStates: list[PreState]
    postconditionStates: list[PostState]

    def recordPreCondition(self, state: Any) -> None:
        """Record a precondition state."""
        if isinstance(state, PreState) and state not in self.preconditionStates:
            self.preconditionStates.append(state)

    def setPreState(self, state: Any) -> None:
        """Set a precondition state (overwrites existing)."""
        if isinstance(state, PreState):
            self.preconditionStates = [state]

    def recordPostCondition(self, state: Any) -> None:
        """Record a postcondition state."""
        if isinstance(state, PostState) and state not in self.postconditionStates:
            self.postconditionStates.append(state)

    def setPostState(self, state: Any) -> None:
        """Set a postcondition state (overwrites existing)."""
        if isinstance(state, PostState):
            self.postconditionStates = [state]

@dataclass
class RunwayId:
    pass

@dataclass
class RunwayCreatedEvent:
    pass

@dataclass
class RunwayUpdatedEvent:
    pass
