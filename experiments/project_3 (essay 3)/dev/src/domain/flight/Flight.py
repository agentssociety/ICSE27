from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from enum import Enum

"""
Domain layer for the Flight domain class

Package: domain.flight
Layer: domain
Related tasks: #72, #76, #77, #78
Requirement coverage:
- Register Flights with Estimated Times
- Runway Closure and Flight Reassignment Management
- Prioritize Emergency Flights and Re-queue Non-Emergency Flights
- Runway Slot Timetable View
"""

@dataclass
class Flight:
    flightNumber: str
    origin: str
    destination: str
    estimatedDepartureTime: str

@dataclass
class Actor:
    mayPerform: set[Permission]
    flight: Flight

@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]
    flight: Flight

@dataclass
class Interface:
    kind: IfaceKind
    encrypted: Bool
    authenticated: Bool

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class State(Enum):
    PRE1 = "pre1"
    POST1 = "post1"
    ERROR = "error"

class IfaceKind(Enum):
    DATABASE = "database"
    UI = "ui"

@dataclass
class Operation:
    pass

@dataclass
class FlightId:
    pass

@dataclass
class FlightCreatedEvent:
    pass

@dataclass
class FlightUpdatedEvent:
    pass
