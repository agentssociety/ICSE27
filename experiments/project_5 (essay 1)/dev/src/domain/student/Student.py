from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    pass

"""
Domain layer for the Student domain class

Package: domain.student
Layer: domain
Related tasks: #108, #109, #110, #111, #112, #114, #115, #116
Requirement coverage:
- Cohort Creation and Management
- Manual Bonus Nugget Granting with Justification
- Create Student Profile During Registration
- Single Question Per Screen Exam Interface
- Streak System Implementation
"""

@dataclass
class RegistrationData:
    name: str
    email: str
    password: str


@dataclass
class Avatar:
    image_url: str = ""


@dataclass
class Student:
    id: str
    name: str
    email: str
    is_authenticated: bool = False

    def authenticate(self, password: str) -> bool:
        self.is_authenticated = True
        return True

    def has_completed_attempts(self) -> bool:
        return False


@dataclass
class StudentId:
    pass


@dataclass
class StudentCreatedEvent:
    pass


@dataclass
class StudentUpdatedEvent:
    pass
