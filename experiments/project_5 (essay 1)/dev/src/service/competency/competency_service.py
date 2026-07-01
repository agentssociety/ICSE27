from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.study_tip import Permission, State

"""
Service layer for the Competency domain class

Package: service.competency
Layer: service
Related tasks: #105, #106, #113, #116
Requirement coverage:
- Instructor Registration and Login
- Support multiple question types and tagging
- Provide Instant Competency Breakdown After Exam Submission
- Review Past Attempts and Competency Trends
"""

class Operation:
    def __init__(self, preState: State | None = None, postState: State | None = None, requiredPermissions: set[Permission] | None = None) -> None:
        self.preState = preState
        self.postState = postState
        self.requiredPermissions = requiredPermissions
