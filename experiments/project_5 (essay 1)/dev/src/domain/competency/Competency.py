from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.question import Question
    from src.domain.study_tip import Actor

"""
Domain layer for the Competency domain class

Package: domain.competency
Layer: domain
Related tasks: #105, #106, #113, #116
Requirement coverage:
- Instructor Registration and Login
- Support multiple question types and tagging
- Provide Instant Competency Breakdown After Exam Submission
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

@dataclass(frozen=True)
class Competency:
    id: str
    name: str
    # Note: questions list is excluded because frozen dataclass can't have mutable lists
    # Use a separate mapping to track question-competency relationships

    def add_question(self, question: Question) -> None:
        pass  # Relationship tracked via Question.competencies

@dataclass
class DifficultyTag:
    resource: Resource
    level: DifficultyTier

    def createTag(self, level: DifficultyTier) -> None:
        self.level = level

@dataclass
class CompetencyId:
    pass

@dataclass
class CompetencyCreatedEvent:
    pass

@dataclass
class CompetencyUpdatedEvent:
    pass
