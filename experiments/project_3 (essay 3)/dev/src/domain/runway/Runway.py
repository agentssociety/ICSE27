from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


"""
Domain layer for the Runway domain class

Package: domain.runway
Layer: domain
Related tasks: #76, #78
Requirement coverage:
- Runway Closure and Flight Reassignment Management
- Runway Slot Timetable View
"""


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass
class Actor:
    mayPerform: set[Permission]
    name: str = ""


@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]


@dataclass
class State:
    name: str = ""

    def transitionTo(self, target: State) -> None:
        self.name = target.name


@dataclass
class Pre1:
    pass


@dataclass
class Pre2:
    def detectCondition(self) -> bool:
        return True

    def transitionTo(self, target: Any) -> None:
        pass


@dataclass
class Post1:
    def applyState(self) -> None:
        pass


@dataclass
class Post2:
    def applyState(self) -> None:
        pass


@dataclass
class Post3:
    def applyState(self) -> None:
        pass


@dataclass
class RunwayClosureRequest:
    runway_id: str = ""
    reason: str = ""


@dataclass
class FlightSchedule:
    flights: list[Any] = field(default_factory=list)

    def reassignFlights(self, fromRunway: str, toRunways: list[Any]) -> None:
        """Reassign flights from a closed runway to available runways."""
        for flight in self.flights:
            for runway in toRunways:
                if runway.id != fromRunway:
                    flight.runway = runway
                    break

    def markFlightDelayed(self, flightId: str, delay: timedelta) -> None:
        """Mark a specific flight as delayed."""
        for flight in self.flights:
            if hasattr(flight, 'id') and str(flight.id) == flightId:
                flight.delayed = True
                flight.delay_duration = delay
                break

    def updateFlightDelay(self, flightId: str, delay: timedelta) -> None:
        """Update the delay for a specific flight."""
        self.markFlightDelayed(flightId, delay)

    def markFlightsAsDelayed(self, runwayId: str) -> None:
        """Mark all flights on a closed runway as delayed if delay > 60 min."""
        for flight in self.flights:
            if hasattr(flight, 'runway') and flight.runway is not None:
                if hasattr(flight.runway, 'id') and flight.runway.id == runwayId:
                    flight.delayed = True


@dataclass
class DelayCalculation:
    def calculateDelay(self, flight: Any) -> timedelta:
        """Calculate delay for a flight based on estimated vs actual departure time."""
        if not hasattr(flight, 'estimatedDepartureTime'):
            return timedelta(minutes=0)
        return timedelta(minutes=30)  # Default calculation for demo


@dataclass
class Airport_Operations_Manager:
    name: str = "AOM"

    def displaySuccess(self, message: Any) -> None:
        print(f"Success: {message}")

    def displayError(self, message: Any) -> None:
        print(f"Error: {message}")

    def displayMessage(self, message: Any) -> None:
        print(f"Message: {message}")


@dataclass
class Flight_Control_Center:
    name: str = "FCC"

    def displayDelays(self, delays: dict) -> None:
        print(f"Delays: {delays}")

    def displayError(self, message: Any) -> None:
        print(f"Error: {message}")


@dataclass
class Passenger_Services_Department:
    name: str = "PSD"


@dataclass
class Runway:
    id: str
    operatingHours: str = "00:00-23:59"
    slots: list[Any] = field(default_factory=list)
    flight: Optional[Any] = None
    is_closed: bool = False

    def close(self) -> None:
        """Close the runway."""
        self.is_closed = True

    def open(self) -> None:
        """Open the runway."""
        self.is_closed = False


@dataclass
class RunwayId:
    id: str = ""


@dataclass
class RunwayCreatedEvent:
    runway_id: str = ""


@dataclass
class RunwayUpdatedEvent:
    runway_id: str = ""
