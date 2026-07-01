from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class Permission(Enum):
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"

class State(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Actor:
    userId: str
    permissions: set[Permission] = field(default_factory=set)

@dataclass
class UserProfile:
    userId: str
    displayName: str

@dataclass
class Follow:
    id: str
    followerId: str
    followingId: str
    state: State = State.ACTIVE
    createdAt: str = ""

@dataclass
class FollowId:
    value: str

@dataclass
class FollowCreatedEvent:
    followId: str

@dataclass
class FollowUpdatedEvent:
    followId: str