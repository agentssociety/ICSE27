from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the ExamSession domain class

Package: service.exam_session
Layer: service
Related tasks: #111
Requirement coverage:
- Single Question Per Screen Exam Interface
"""

class ExamSessionService(Protocol):
    ...

class ExamSessionServiceImpl:
    def __init__(self) -> None:
        pass
