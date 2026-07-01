from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NotificationCreate(NotificationBase):
    like_id: int
    comment_id: int


class NotificationUpdate(NotificationBase):
    like_id: Optional[int] = None
    comment_id: Optional[int] = None


class NotificationResponse(NotificationBase):
    id: int
    like_id: Optional[int] = None
    comment_id: Optional[int] = None
