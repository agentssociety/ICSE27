from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.study_tip import Permission, State

"""
Service layer for the ExamBuilder domain class

Package: service.exam_builder
Layer: service
Related tasks: #106
Requirement coverage:
- Support multiple question types and tagging
"""

class Operation:
    def __init__(self, preState: State | None = None, postState: State | None = None, requiredPermissions: set[Permission] | None = None) -> None:
        self.preState = preState
        self.postState = postState
        self.requiredPermissions = requiredPermissions
