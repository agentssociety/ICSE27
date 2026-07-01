from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING
from enum import Enum
from uuid import UUID
from dataclasses import dataclass, field
from datetime import date as Date

if TYPE_CHECKING:
    from src.domain.competency import Competency
    from src.domain.student import Student
    from src.domain.study_tip import Actor

@dataclass
class Attempt:
    attempt_id: str = ""
    exam_id: str = ""
    score: float = 0.0
    date: str = ""

@dataclass
class ChartPoint:
    date: str = ""
    score: float = 0.0

@dataclass
class PastAttemptData:
    studentId: UUID | None = None
    attempts: list[Attempt] | None = None
    totalAttempts: int | None = None
    lastAttemptDate: Date | None = None

    def verifyAccess(self, student: Student) -> bool:
        if self.studentId and student:
            return str(self.studentId) == student.id
        return True

@dataclass
class DashboardData:
    studentId: UUID | None = None
    recentAttempts: list[Attempt] | None = None
    competencies: list[Any] | None = None
    overallProgress: float | None = None

    def createFromAttempts(self, attempts: list[Attempt]) -> DashboardData:
        scores = [a.score for a in attempts] if attempts else []
        return DashboardData(
            studentId=self.studentId,
            recentAttempts=attempts,
            competencies=self.competencies,
            overallProgress=sum(scores) / len(scores) if scores else 0.0
        )

    def verifyAccess(self, actor: Actor) -> bool:
        return True

@dataclass
class TrendData:
    studentId: UUID | None = None
    competencyId: UUID | None = None
    chartPoints: list[ChartPoint] | None = None
    trendDirection: str | None = None
    sufficientData: bool | None = None

class ReviewService(Protocol):
    def get_past_attempts(self, student_id: str) -> list[Attempt]:
        ...
    def get_dashboard(self, student_id: str) -> DashboardData:
        ...
    def get_trend(self, student_id: str, competency_id: str) -> TrendData:
        ...

class AccessControlService(Protocol):
    def check_access(self, actor: Any, resource: Any) -> bool:
        ...

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class Role(Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    LMS_TEAM = "lms_team"
