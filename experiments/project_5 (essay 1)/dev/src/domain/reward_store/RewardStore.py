from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field

@dataclass
class RewardStore:
    name: str
    description: str = ""
    items: list[Any] = field(default_factory=list)

@dataclass
class RewardStoreId:
    pass

@dataclass
class RewardStoreCreatedEvent:
    pass

@dataclass
class RewardStoreUpdatedEvent:
    pass
