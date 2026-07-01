from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class FriendRequestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FriendRequestCreate(FriendRequestBase):
    pending: bool
    abstract_isDuplicate: bool
    abstract_validateRequest: None
    notification_id: int


class FriendRequestUpdate(FriendRequestBase):
    pending: Optional[bool] = None
    abstract_isDuplicate: Optional[bool] = None
    abstract_validateRequest: Optional[None] = None
    notification_id: Optional[int] = None


class FriendRequestResponse(FriendRequestBase):
    id: int
    pending: bool
    abstract_isDuplicate: bool
    abstract_validateRequest: None
    notification_id: Optional[int] = None
