from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.user import Actor, User


"""
Domain layer for the PIN domain class

Package: domain.pin
Layer: domain
Related tasks: None
"""


@dataclass
class PIN:
    owner: "Actor"
    accessible: set["Actor"] = field(default_factory=set)
    user: "User" = None

    def validate(self, pinData: str) -> bool:
        return bool(pinData)


@dataclass
class PINId:
    pass


@dataclass
class PINCreatedEvent:
    pass


@dataclass
class PINUpdatedEvent:
    pass
