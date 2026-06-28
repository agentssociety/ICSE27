from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING, Set, FrozenSet as frozenset
from dataclasses import dataclass
from enum import Enum, IntEnum

if TYPE_CHECKING:
    from src.domain.patient import Patient

"""
Domain layer for the UrgencyLevel domain class

Package: domain.urgency_level
Layer: domain
Related tasks: #54, #55, #56, #58
Requirement coverage:
- Assign Item Urgency Level
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Real-time live dashboard displaying urgency and wait time
"""


class UrgencyLevelValue(IntEnum):
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    HIGHEST = 5


@dataclass
class UrgencyLevel:
    level: int

    def __post_init__(self) -> None:
        if not 1 <= self.level <= 5:
            raise ValueError(f"Urgency level must be between 1 and 5, got {self.level}")

    @property
    def label(self) -> str:
        labels = {
            1: "Lowest",
            2: "Low",
            3: "Medium",
            4: "High",
            5: "Highest",
        }
        return labels[self.level]

    def increase(self) -> UrgencyLevel:
        if self.level >= 5:
            raise ValueError("Cannot increase urgency above 5")
        return UrgencyLevel(level=self.level + 1)

    def decrease(self) -> UrgencyLevel:
        if self.level <= 1:
            raise ValueError("Cannot decrease urgency below 1")
        return UrgencyLevel(level=self.level - 1)


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass(frozen=True, eq=True)
class Actor:
    mayPerform: frozenset[Permission]

    def hasPermission(self, permission: Permission) -> bool:
        return permission in self.mayPerform


@dataclass
class Resource:
    owner: Actor
    accessible: Set[Actor]
    urgency: Optional[UrgencyLevel] = None

    def findResource(self, resourceId: str) -> Resource:
        return self

    def isInAccessibleSet(self, actor: Actor) -> bool:
        return actor in self.accessible

    def setUrgency(self, urgency: UrgencyLevel) -> Resource:
        self.urgency = urgency
        return self

    def validateOwnerInAccessible(self) -> None:
        if self.owner not in self.accessible:
            raise PermissionError("Owner must be in accessible set")

    def saveState(self) -> None:
        pass

    def checkVersion(self, resource: Resource) -> bool:
        return True


@dataclass
class State:
    state_data: Any = None

    def getPreState(self) -> State:
        return State()

    def transitionTo(self, Post1: Any) -> bool:
        return True

    def updateState(self) -> None:
        pass

    def getPostState(self) -> State:
        return State()


@dataclass
class Interface:
    kind: str
    encrypted: bool
    authenticated: bool


@dataclass
class UrgencyLevelId:
    pass


@dataclass
class UrgencyLevelCreatedEvent:
    pass


@dataclass
class UrgencyLevelUpdatedEvent:
    pass
