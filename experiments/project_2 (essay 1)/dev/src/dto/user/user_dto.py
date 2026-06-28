from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    userId: str


class UserUpdate(UserBase):
    userId: Optional[str] = None


class UserResponse(UserBase):
    userId: str
