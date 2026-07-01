from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.user import User

"""
Domain layer for the Block domain class

Package: domain.block
Layer: domain
Related tasks: #175
Requirement coverage:
- User must be able to block another user to hide their posts and messages
"""

@dataclass
class BlockRecord:
    blocker: User
    blocked: User

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
class Block:
    user: Optional[User] = None

@dataclass
class BlockId:
    pass

@dataclass
class BlockCreatedEvent:
    pass

@dataclass
class BlockUpdatedEvent:
    pass
