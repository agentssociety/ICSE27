from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.study_tip import Permission, State

"""
Service layer for the Question domain class

Package: service.question
Layer: service
Related tasks: #106, #111, #116
Requirement coverage:
- Support multiple question types and tagging
- Single Question Per Screen Exam Interface
- Review Past Attempts and Competency Trends
"""

class Operation:
    def __init__(self, preState: State | None = None, postState: State | None = None, requiredPermissions: set[Permission] | None = None) -> None:
        self.preState = preState
        self.postState = postState
        self.requiredPermissions = requiredPermissions
