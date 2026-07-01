from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    pass

"""
Service layer for the Student domain class

Package: service.student
Layer: service
Related tasks: #108, #109, #110, #111, #112, #114, #115, #116
Requirement coverage:
- Cohort Creation and Management
- Manual Bonus Nugget Granting with Justification
- Create Student Profile During Registration
- Single Question Per Screen Exam Interface
- Streak System Implementation
"""

class RegistrationService(Protocol):
    def register(self, input: RegistrationInput) -> str:
        ...

    def validate_input(self, input: RegistrationInput) -> bool:
        ...

class RegistrationInput:
    def __init__(self, name: str | None = None, email: str | None = None, password: str | None = None) -> None:
        self.name = name
        self.email = email
        self.password = password

    def get_name(self) -> str:
        return self.name or ""

    def get_email(self) -> str:
        return self.email or ""

    def get_password(self) -> str:
        return self.password or ""
