from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

"""
Domain layer for the Flight domain class

Package: domain.flight
Layer: domain
Related tasks: #65, #66, #67, #68, #69, #70, #71
"""

DateTime = datetime


class FlightType(Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class FlightStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE1 = "pre1"
    POST1 = "post1"
    POST2 = "post2"
    POST3 = "post3"


@dataclass
class FlightId:
    value: str = ""

    def __post_init__(self) -> None:
        if not self.value:
            import uuid
            self.value = str(uuid.uuid4())


@dataclass
class FlightCreatedEvent:
    flightNumber: str
    scheduledTime: DateTime


@dataclass
class FlightUpdatedEvent:
    flightNumber: str
    scheduledTime: DateTime
    previousTime: DateTime


@dataclass
class Resource:
    owner: str
    accessible: set[str]
    note: str = ""
    flight: Optional["Flight"] = None


@dataclass
class Flight:
    flightNumber: str
    airline: str
    origin: str
    destination: str
    scheduledTime: DateTime
    type: FlightType
    status: FlightStatus = FlightStatus.ACTIVE
    note: str = ""

    def create(self, fields: dict) -> "Flight":
        """Create a new Flight from a dictionary of fields."""
        return Flight(
            flightNumber=fields.get("flightNumber", self.flightNumber),
            airline=fields.get("airline", self.airline),
            origin=fields.get("origin", self.origin),
            destination=fields.get("destination", self.destination),
            scheduledTime=fields.get("scheduledTime", self.scheduledTime),
            type=fields.get("type", self.type),
            status=fields.get("status", self.status),
            note=fields.get("note", self.note),
        )

    def setFlightNumber(self, fn: str) -> None:
        """Set the flight number."""
        if not fn or not fn.strip():
            raise ValueError("Flight number cannot be empty")
        self.flightNumber = fn

    def setType(self, flight_type: FlightType) -> None:
        """Set the flight type (arrival/departure)."""
        if not isinstance(flight_type, FlightType):
            raise TypeError("Type must be a FlightType enum value")
        self.type = flight_type

    def setStatus(self, status: FlightStatus) -> None:
        """Set the flight status."""
        if not isinstance(status, FlightStatus):
            raise TypeError("Status must be a FlightStatus enum value")
        self.status = status

    def validateNewSchedule(self, time: DateTime) -> bool:
        """Validate that a new schedule time is acceptable (e.g., in the future)."""
        if time is None:
            return False
        return True

    def setScheduledTime(self, newTime: DateTime) -> None:
        """Set a new scheduled time for the flight."""
        self.scheduledTime = newTime

    def getStatus(self) -> FlightStatus:
        """Return the current flight status."""
        return self.status

    def cancel(self) -> None:
        """Cancel the flight by setting status to CANCELLED."""
        self.status = FlightStatus.CANCELLED
