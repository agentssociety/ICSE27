from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.competency import Competency
    from src.domain.study_tip import Actor

"""
Domain layer for the Question domain class

Package: domain.question
Layer: domain
Related tasks: #106, #111, #116
Requirement coverage:
- Support multiple question types and tagging
- Single Question Per Screen Exam Interface
- Review Past Attempts and Competency Trends
"""

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    DRAG_AND_DROP = "drag_and_drop"
    CODE_SNIPPET = "code_snippet"

class DifficultyTier(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST_ERROR = "post_error"

@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]

@dataclass
class DifficultyTag:
    resource: Resource
    level: DifficultyTier

    def createTag(self, level: DifficultyTier) -> None:
        self.level = level

@dataclass
class Question:
    type: QuestionType
    competencies: set[Competency] = field(default_factory=set)
    difficultyTier: DifficultyTier = DifficultyTier.BEGINNER
    nuggetRewardMultiplier: Optional[float] = None

    def add_competency(self, competency: Competency) -> None:
        self.competencies.add(competency)

    def remove_competency(self, competency: Competency) -> None:
        self.competencies.discard(competency)

    def set_difficulty(self, tier: DifficultyTier) -> None:
        self.difficultyTier = tier

    def set_nugget_multiplier(self, multiplier: float) -> None:
        if multiplier < 0:
            raise ValueError("Nugget reward multiplier must be non-negative")
        self.nuggetRewardMultiplier = multiplier

    def setState(self, post1: Any) -> None:
        pass

@dataclass
class QuestionId:
    pass

@dataclass
class QuestionCreatedEvent:
    pass

@dataclass
class QuestionUpdatedEvent:
    pass
