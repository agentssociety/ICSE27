from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class StudyTip:
    competency_id: str
    title: str
    content: str = ""
    difficulty_level: str = "beginner"

@dataclass
class StudyTipId:
    pass

@dataclass
class StudyTipCreatedEvent:
    pass

@dataclass
class StudyTipUpdatedEvent:
    pass
