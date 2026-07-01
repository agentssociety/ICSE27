from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class NotificationPreferenceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceCreate(NotificationPreferenceBase):
    userId: str
    enabled: bool


class NotificationPreferenceUpdate(NotificationPreferenceBase):
    userId: Optional[str] = None
    enabled: Optional[bool] = None


class NotificationPreferenceResponse(NotificationPreferenceBase):
    userId: str
    userId: str
    enabled: bool
