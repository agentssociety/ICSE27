from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class LockoutNotificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LockoutNotificationCreate(LockoutNotificationBase):
    lockout_id: int


class LockoutNotificationUpdate(LockoutNotificationBase):
    lockout_id: Optional[int] = None


class LockoutNotificationResponse(LockoutNotificationBase):
    id: int
    lockout_id: Optional[int] = None
