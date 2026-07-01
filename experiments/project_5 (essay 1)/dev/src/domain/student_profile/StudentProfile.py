from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

"""
Domain layer for the StudentProfile domain class

Package: domain.student_profile
Layer: domain
Related tasks: #110
Requirement coverage:
- Create Student Profile During Registration
"""


@dataclass
class StudentProfile:
    student_id: str
    avatar_url: str = ""
    bio: str = ""
    preferences: dict[str, Any] | None = None

@dataclass
class StudentProfileId:
    pass

@dataclass
class StudentProfileCreatedEvent:
    pass

@dataclass
class StudentProfileUpdatedEvent:
    pass
