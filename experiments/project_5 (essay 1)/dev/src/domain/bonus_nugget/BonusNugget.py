from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class BonusNugget:
    student_id: str
    amount: float
    reason: str = ""
    granted_by: str = ""
    granted_at: str = ""

@dataclass
class BonusNuggetId:
    pass

@dataclass
class BonusNuggetCreatedEvent:
    pass

@dataclass
class BonusNuggetUpdatedEvent:
    pass
