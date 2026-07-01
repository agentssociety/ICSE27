from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

"""
Domain layer for the Badge domain class

Package: domain.badge
Layer: domain
Related tasks: #110
Requirement coverage:
- Create Student Profile During Registration
"""


@dataclass
class Badge:
    name: str
    description: str = ""
    icon_url: str = ""

    def display(self) -> str:
        return f"{self.name}: {self.description}"

@dataclass
class BadgeId:
    pass

@dataclass
class BadgeCreatedEvent:
    pass

@dataclass
class BadgeUpdatedEvent:
    pass
