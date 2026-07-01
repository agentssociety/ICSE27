from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.post import Post
    from src.domain.user import User

"""
Domain layer for the Like domain class

Package: domain.like
Layer: domain
Related tasks: #160, #169
Requirement coverage:
- User can like and unlike a post
- User receives notification on post interactions
"""

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"

@dataclass
class Actor:
    field_mayPerform: set[Permission]
    user: User

@dataclass
class Resource:
    field_owner: Actor
    field_accessible: set[Actor]
    post: Post

@dataclass
class Like:
    user: User
    post: Post

@dataclass
class LikeId:
    pass

@dataclass
class LikeCreatedEvent:
    pass

@dataclass
class LikeUpdatedEvent:
    pass
