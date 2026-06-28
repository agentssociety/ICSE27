from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    userID: str
    card_id: int
    pIN_id: int
    account_id: int


class UserUpdate(UserBase):
    userID: Optional[str] = None
    card_id: Optional[int] = None
    pIN_id: Optional[int] = None
    account_id: Optional[int] = None


class UserResponse(UserBase):
    userID: str
    card_id: Optional[int] = None
    pIN_id: Optional[int] = None
    account_id: Optional[int] = None
