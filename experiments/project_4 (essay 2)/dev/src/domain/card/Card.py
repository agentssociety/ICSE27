from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.account import Admin, StateValue
    from src.domain.pin import Pin

"""
Domain layer for the Card domain class

Package: domain.card
Layer: domain
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE_IDLE = "pre_idle"
    POST_1 = "post_1"
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    PRE1 = "pre1"
    PRE2 = "pre2"
    PRE3 = "pre3"
    POST1 = "post1"
    POST2 = "post2"
    PREIDLE = "preidle"
    POST3 = "post3"


class IfaceKind(Enum):
    HARDWARE_INTERFACE = "hardware_interface"
    SERVICE_INTERFACE = "service_interface"


class Bool(Enum):
    TRUE_ = "true_"
    FALSE_ = "false_"


@dataclass
class Actor:
    mayPerform: set[Permission]
    note_mayPerform_assignment: str = ""

    def getActorByCard(self, cardData: str) -> Actor:
        # Simulate looking up an actor by card data
        return Actor(mayPerform={Permission.READ})

    def mayPerform(self, grant_Admin: Any) -> bool:
        return Permission.ADMIN in self.mayPerform


@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]


@dataclass
class Credential:
    actor: Actor
    pin: Pin

    def getCredential(self, actor: Actor) -> Credential:
        return Credential(actor=actor, pin=self.pin)


@dataclass
class Digit:
    pin: Pin

    def transition(self, from_state: Any, to_state: Any) -> bool:
        return True


@dataclass
class Card:
    pass


@dataclass
class CardId:
    pass


@dataclass
class CardCreatedEvent:
    pass


@dataclass
class CardUpdatedEvent:
    pass
