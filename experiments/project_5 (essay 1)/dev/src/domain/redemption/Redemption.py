from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class Redemption:
    student_id: str
    reward_item_id: str
    redeemed_at: str = ""

@dataclass
class RedemptionId:
    pass

@dataclass
class RedemptionCreatedEvent:
    pass

@dataclass
class RedemptionUpdatedEvent:
    pass
