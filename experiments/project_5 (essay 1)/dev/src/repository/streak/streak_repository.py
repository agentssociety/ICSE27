from __future__ import annotations

from typing import Any, Protocol
from enum import Enum

"""
Repository layer for the Streak domain class

Package: repository.streak
Layer: repository
Related tasks: #112
Requirement coverage:
- Streak System Implementation
"""

class Actor(Protocol):
    def hasPermission(self, Permission_Write: Any) -> None:
        ...

class Resource(Protocol):
    def isAccessible(self, A: Any) -> None:
        ...

class Interface(Protocol):
    ...

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

class State(Enum):
    ANSWERING = "answering"
    CORRECTFIRSTTIME = "correctfirsttime"
    INCORRECTRESET = "incorrectreset"
    NEXTCORRECT1_5X = "nextcorrect1_5x"
    NEXTCORRECT2X = "nextcorrect2x"
    NEXTCORRECT3X = "nextcorrect3x"

class IfaceKind(Enum):
    DATABASE = "database"
    API = "api"
    UI = "ui"
