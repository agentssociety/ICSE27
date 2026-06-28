from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class UserAuthenticationSystemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserAuthenticationSystemCreate(UserAuthenticationSystemBase):
    sessionToken: str
    userId: str
    patient_id: int


class UserAuthenticationSystemUpdate(UserAuthenticationSystemBase):
    sessionToken: Optional[str] = None
    userId: Optional[str] = None
    patient_id: Optional[int] = None


class UserAuthenticationSystemResponse(UserAuthenticationSystemBase):
    userId: str
    sessionToken: str
    userId: str
    patient_id: Optional[int] = None
