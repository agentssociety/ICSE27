from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from src.domain.flight.Flight import Flight


DateTime = datetime


class RunwayStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    MAINTENANCE = "maintenance"


class AircraftType(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    HEAVY = "heavy"


class PermissionLevel(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class RunwayId:
    value: str = ""

    def __post_init__(self) -> None:
        if not self.value:
            import uuid
            self.value = str(uuid.uuid4())


@dataclass
class RunwayCreatedEvent:
    runwayId: str


@dataclass
class RunwayUpdatedEvent:
    runwayId: str


@dataclass
class Runway:
    runwayId: str
    status: RunwayStatus = RunwayStatus.OPEN
    length: int = 3000
    aircraftTypes: set[AircraftType] = field(default_factory=lambda: {AircraftType.SMALL, AircraftType.MEDIUM, AircraftType.LARGE})
    flights: list[Flight] = field(default_factory=list)
    timeSlot: Optional[Any] = None

    def close(self) -> None:
        """Mark the runway as closed."""
        self.status = RunwayStatus.CLOSED

    def is_closed(self) -> bool:
        """Check if the runway is closed."""
        return self.status == RunwayStatus.CLOSED

    def is_available_for(self, aircraft_type: AircraftType) -> bool:
        """Check if this runway is available for a given aircraft type."""
        return self.status == RunwayStatus.OPEN and aircraft_type in self.aircraftTypes


@dataclass
class Slot:
    time: DateTime
    flight: Flight
    runway: Runway

    def updateSlot(self, runway: Any, time: DateTime) -> None:
        self.runway = runway
        self.time = time


@dataclass
class AlternativeRunway:
    compatibleFlightTypes: set[AircraftType]
    runway: Runway
    isAvailable: bool = True

    def is_available(self) -> bool:
        return self.isAvailable and self.runway.status == RunwayStatus.OPEN


@dataclass
class Operation:
    description: str


@dataclass
class Resource:
    resourceId: str
    resourceType: str


@dataclass
class Channel:
    channelId: str
    channelType: str


@dataclass
class Interface:
    name: str
    description: str
    securityRequirements: str
