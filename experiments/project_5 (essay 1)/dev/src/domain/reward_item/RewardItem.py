from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class RewardItem:
    name: str
    cost: float
    description: str = ""
    image_url: str = ""

@dataclass
class RewardItemId:
    pass

@dataclass
class RewardItemCreatedEvent:
    pass

@dataclass
class RewardItemUpdatedEvent:
    pass
