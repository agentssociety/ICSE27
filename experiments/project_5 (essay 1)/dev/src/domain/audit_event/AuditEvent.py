from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.instructor import Instructor
    from src.domain.nugget_wallet import NuggetWallet
    from src.domain.student import Student

"""
Domain layer for the AuditEvent domain class

Package: domain.audit_event
Layer: domain
Related tasks: #109
Requirement coverage:
- Manual Bonus Nugget Granting with Justification
"""

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    BONUS_GRANT = "bonus_grant"

class State(Enum):
    PRE1 = "pre1"
    JUSTIFIED_STATE = "justified_state"
    POST1 = "post1"
    POST2 = "post2"
    ERROR_STATE = "error_state"

@dataclass
class Teacher:
    id: str
    name: str
    mayPermit: list[Permission]

@dataclass
class IT_Team:
    id: str
    mayPermit: list[Permission]

@dataclass
class BonusNugget:
    amount: int
    justification: str
    teacherId: str
    studentId: str
    timestamp: DateTime
    student: Student
    auditEvent: AuditEvent

@dataclass
class Justification:
    text: str
    teacherId: str

@dataclass
class AuditEvent:
    eventId: str
    teacherId: str
    studentId: str
    amount: int
    justification: str
    timestamp: DateTime
    instructor: Optional[Instructor] = None
    nuggetWallet: Optional[NuggetWallet] = None
    student: Optional[Student] = None

@dataclass
class AuditEventId:
    pass

@dataclass
class AuditEventCreatedEvent:
    pass

@dataclass
class AuditEventUpdatedEvent:
    pass
