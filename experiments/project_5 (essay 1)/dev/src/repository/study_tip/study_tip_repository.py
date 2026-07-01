from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.repository.streak import IfaceKind

"""
Repository layer for the StudyTip domain class

Package: repository.study_tip
Layer: repository
Related tasks: #113
Requirement coverage:
- Provide Instant Competency Breakdown After Exam Submission
"""

class Interface(Protocol):
    def validateChannel(self, channel: Interface) -> bool:
        ...

class Exam_Analysis_API(Protocol):
    ...

class Student_Dashboard(Protocol):
    ...
