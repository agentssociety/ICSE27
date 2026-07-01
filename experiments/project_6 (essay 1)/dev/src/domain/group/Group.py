from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class Visibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class State(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class Operation(Enum):
    JOIN = "join"
    LEAVE = "leave"
    POST = "post"

@dataclass
class GroupName:
    value: str

@dataclass
class Group:
    id: str
    name: str
    description: str = ""
    visibility: Visibility = Visibility.PUBLIC
    ownerId: str = ""
    state: State = State.ACTIVE
    memberCount: int = 0
    createdAt: str = ""

    def canJoin(self, userId: str) -> bool:
        return self.visibility == Visibility.PUBLIC and self.state == State.ACTIVE

@dataclass
class GroupId:
    value: str

@dataclass
class GroupCreatedEvent:
    groupId: str

@dataclass
class GroupUpdatedEvent:
    groupId: str
