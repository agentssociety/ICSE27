from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserProfileCreate(UserProfileBase):
    verifiedBadgeStatus: bool


class UserProfileUpdate(UserProfileBase):
    verifiedBadgeStatus: Optional[bool] = None


class UserProfileResponse(UserProfileBase):
    id: int
    verifiedBadgeStatus: bool
