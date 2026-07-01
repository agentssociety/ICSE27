from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.study_tip import Actor
    from src.domain.question import Question

"""
Domain layer for the ExamBuilder domain class

Package: domain.exam_builder
Layer: domain
Related tasks: #106
Requirement coverage:
- Support multiple question types and tagging
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
class ExamBuilder:
    questions: list[Question] = field(default_factory=list)

    def create_question(self, question: Question) -> None:
        if not question:
            raise ValueError("Question cannot be None")
        self.questions.append(question)

    def get_questions_by_type(self, question_type: QuestionType) -> list[Question]:
        return [q for q in self.questions if q.type == question_type]

    def get_questions_by_difficulty(self, difficulty: DifficultyTier) -> list[Question]:
        return [q for q in self.questions if q.difficultyTier == difficulty]

@dataclass
class ExamBuilderId:
    pass

@dataclass
class ExamBuilderCreatedEvent:
    pass

@dataclass
class ExamBuilderUpdatedEvent:
    pass
