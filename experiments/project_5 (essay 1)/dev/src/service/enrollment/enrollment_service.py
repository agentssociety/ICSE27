from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Enrollment domain class

Package: service.enrollment
Layer: service
Related tasks: #105, #108
Requirement coverage:
- Instructor Registration and Login
- Cohort Creation and Management
"""

class EnrollmentService(Protocol):
    ...

class EnrollmentServiceImpl:
    def __init__(self) -> None:
        pass
