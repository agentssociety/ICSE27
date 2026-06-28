from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime as DateTime

"""
Domain layer for the Flight domain class

Package: domain.flight
Layer: domain
Related tasks: #46, #48, #49, #50, #51, #52
Requirement coverage:
- Register Incoming Flights
- Priority Slot Allocation for Arrival Flights
- Prevent Overlapping Flight Assignments
- Automatic Reassignment of Flights During Runway Closure
- Handle Emergency Flights
"""

@dataclass
class Flight:
    flightNumber: str
    aircraftType: str
    scheduledTime: DateTime
    direction: Direction

    @staticmethod
    def create(flightNumber: str, aircraftType: str, scheduledTime: DateTime, direction: Direction) -> "Flight":
        """Factory method to create a new Flight instance with validation."""
        if not flightNumber or not flightNumber.strip():
            raise ValueError("flightNumber must be a non-empty string")
        if not aircraftType or not aircraftType.strip():
            raise ValueError("aircraftType must be a non-empty string")
        if not isinstance(scheduledTime, DateTime):
            raise ValueError("scheduledTime must be a datetime object")
        if not isinstance(direction, Direction):
            raise ValueError("direction must be a Direction enum value")
        return Flight(
            flightNumber=flightNumber.strip(),
            aircraftType=aircraftType.strip(),
            scheduledTime=scheduledTime,
            direction=direction,
        )

class Direction(Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

@dataclass
class AircraftMovementLog:
    entries: list[Flight] = field(default_factory=list)

    def add_entry(self, flight: Flight) -> None:
        self.entries.append(flight)

    def get_all_entries(self) -> list[Flight]:
        return list(self.entries)

@dataclass
class Operation:
    initiator: Actor
    target: list[Resource]
    channel: list[Interface]
    grant: Permission
    pre: State
    post: State

    @staticmethod
    def create(initiator: Actor, target: list[Resource], channel: list[Interface], grant: Permission, pre: State, post: State) -> "Operation":
        """Factory method to create an Operation."""
        if not isinstance(initiator, Actor):
            raise ValueError("initiator must be an Actor")
        if not isinstance(target, list) or not all(isinstance(r, Resource) for r in target):
            raise ValueError("target must be a list of Resource")
        if not isinstance(channel, list) or not all(isinstance(c, Interface) for c in channel):
            raise ValueError("channel must be a list of Interface")
        if not isinstance(grant, Permission):
            raise ValueError("grant must be a Permission")
        if not isinstance(pre, State):
            raise ValueError("pre must be a State")
        if not isinstance(post, State):
            raise ValueError("post must be a State")
        return Operation(
            initiator=initiator,
            target=target,
            channel=channel,
            grant=grant,
            pre=pre,
            post=post,
        )

@dataclass
class Actor:
    mayPerform: list[Permission]

@dataclass
class Resource:
    owner: Actor
    accessible: list[Actor]

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    CONSTRAINT_READ_WRITE_EXECUTE_ADMIN = "constraint_read_write_execute_admin"

class State(Enum):
    PRE1 = "pre1"
    POST1 = "post1"
    POST2 = "post2"
    POST3 = "post3"

@dataclass
class Interface:
    kind: InterfaceKind
    encrypted: bool
    authenticated: bool

class InterfaceKind(Enum):
    API = "api"
    DATABASE = "database"

@dataclass
class FlightId:
    pass

@dataclass
class FlightCreatedEvent:
    pass

@dataclass
class FlightUpdatedEvent:
    pass
