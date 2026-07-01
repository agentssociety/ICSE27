from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Instructor domain class

Package: service.instructor
Layer: service
Related tasks: #105
Requirement coverage:
- Instructor Registration and Login
"""

class InstructorService(Protocol):
    ...

class InstructorServiceImpl:
    def __init__(self) -> None:
        pass
