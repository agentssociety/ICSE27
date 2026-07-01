from __future__ import annotations

from typing import Any
from pydantic import BaseModel

"""
Dto layer for the InstructorDashboard domain class

Package: dto.instructor_dashboard
Layer: dto
Related tasks: #105
Requirement coverage:
- Instructor Registration and Login
"""

class InstructorDashboardCreateRequest(BaseModel):
    pass

class InstructorDashboardUpdateRequest(BaseModel):
    pass

class InstructorDashboardResponse(BaseModel):
    pass