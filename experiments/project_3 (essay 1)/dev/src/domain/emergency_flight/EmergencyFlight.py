from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
from datetime import datetime as DateTime

if TYPE_CHECKING:
    from src.domain.flight import Flight
    from src.domain.slot import Slot

"""
Domain layer for the EmergencyFlight domain class

Package: domain.emergency_flight
Layer: domain
Related tasks: #51
Requirement coverage:
- Handle Emergency Flights
"""

class FlightType(Enum):
    EMERGENCY = "emergency"
    NON_EMERGENCY = "non_emergency"

class SlotStatus(Enum):
    AVAILABLE = "available"
    ALLOCATED = "allocated"

@dataclass
class FlightQueue:
    flights: list["Flight"]

    def insertEmergencyFlight(self, emergency: "EmergencyFlight", slot: "Slot") -> None:
        """Insert an emergency flight into the queue at the front position (position 0)."""
        if emergency.flight not in self.flights:
            self.flights.insert(0, emergency.flight)

    def reQueueFlights(self, excludeEmergency: "Flight") -> list["Flight"]:
        """Re-queue all flights except the given emergency flight, maintaining order."""
        requeued = [f for f in self.flights if f != excludeEmergency]
        self.flights = requeued
        return list(requeued)

    def reQueueAllNonEmergency(self) -> None:
        """Re-queue all non-emergency flights."""
        non_emergency = [f for f in self.flights if hasattr(f, 'flightType') and f.flightType == FlightType.NON_EMERGENCY]
        self.flights = non_emergency

    def removeFlight(self, flight: "Flight") -> None:
        """Remove a specific flight from the queue."""
        self.flights = [f for f in self.flights if f != flight]

    def insertFlightAtPosition(self, flight: "Flight", position: int) -> None:
        """Insert a flight at a specific position in the queue."""
        position = max(0, min(position, len(self.flights)))
        if flight not in self.flights:
            self.flights.insert(position, flight)

@dataclass
class EmergencyFlight:
    id: str
    detectionTime: DateTime
    flight: "Flight"
    slot: Optional["Slot"] = None

    @staticmethod
    def create(id: str, detectionTime: DateTime, flight: "Flight", slot: Optional["Slot"] = None) -> "EmergencyFlight":
        """Factory method to create an EmergencyFlight with validation."""
        if not id or not id.strip():
            raise ValueError("id must be a non-empty string")
        if not isinstance(detectionTime, DateTime):
            raise ValueError("detectionTime must be a datetime object")
        return EmergencyFlight(
            id=id.strip(),
            detectionTime=detectionTime,
            flight=flight,
            slot=slot,
        )

    def __post_init__(self) -> None:
        """Validate after dataclass initialization."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("id must be a non-empty string")

@dataclass
class EmergencyFlightId:
    pass

@dataclass
class EmergencyFlightCreatedEvent:
    pass

@dataclass
class EmergencyFlightUpdatedEvent:
    pass
