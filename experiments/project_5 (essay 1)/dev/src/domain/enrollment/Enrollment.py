from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

"""
Domain layer for the Enrollment domain class

Package: domain.enrollment
Layer: domain
Related tasks: #105, #108
Requirement coverage:
- Instructor Registration and Login
- Cohort Creation and Management
"""


@dataclass
class Enrollment:
    student_id: str
    cohort_id: str
    enrolled_at: str = ""

@dataclass
class EnrollmentId:
    pass

@dataclass
class EnrollmentCreatedEvent:
    pass

@dataclass
class EnrollmentUpdatedEvent:
    pass
