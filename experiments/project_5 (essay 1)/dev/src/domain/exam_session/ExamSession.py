from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    pass

"""
Domain layer for the ExamSession domain class

Package: domain.exam_session
Layer: domain
Related tasks: #111
Requirement coverage:
- Single Question Per Screen Exam Interface
"""


@dataclass
class Exam:
    id: str
    title: str
    questions: list[Any]
    timer_duration: int = 0
    current_question_index: int = 0
    progress: str = ""


@dataclass
class ExamSession:
    student_id: str
    exam_id: str
    start_time: str = ""
    end_time: str = ""
    answers: dict[str, str] | None = None
    status: str = "in_progress"

    def record_answer(self, question_id: str, answer: str) -> None:
        if self.answers is None:
            self.answers = {}
        self.answers[question_id] = answer

    def end_exam(self) -> None:
        self.status = "completed"


class ExamStatus(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class ExamSessionId:
    pass


@dataclass
class ExamSessionCreatedEvent:
    pass


@dataclass
class ExamSessionUpdatedEvent:
    pass
