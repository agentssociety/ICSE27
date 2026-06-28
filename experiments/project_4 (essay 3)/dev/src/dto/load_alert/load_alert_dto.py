from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class LoadAlertBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoadAlertCreate(LoadAlertBase):
    channel: str
    highLoad: bool


class LoadAlertUpdate(LoadAlertBase):
    channel: Optional[str] = None
    highLoad: Optional[bool] = None


class LoadAlertResponse(LoadAlertBase):
    id: int
    channel: str
    highLoad: bool
