from __future__ import annotations

from typing import Any
from pydantic import BaseModel

"""
Dto layer for the Instructor domain class

Package: dto.instructor
Layer: dto
Related tasks: #105
Requirement coverage:
- Instructor Registration and Login
"""

class InstructorCreateRequest(BaseModel):
    pass

class InstructorUpdateRequest(BaseModel):
    pass

class InstructorResponse(BaseModel):
    pass