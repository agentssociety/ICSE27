from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict

"""
Dto layer for the User domain class

Package: dto.user
Layer: dto
Related tasks: #88, #89, #93, #94, #95
Requirement coverage:
- Card and PIN Authentication Requirement
- Account Lock After Three Consecutive Failed PIN Attempts
- Admin Interface for Flagged Transactions Review
- Manual Lock/Unlock User Accounts
- Audit Log Maintenance
"""


class UserCreateRequest(BaseModel):
    name: str
    email: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    is_active: bool
