from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SlotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SlotCreate(SlotBase):
    resource_id: Optional[int] = None
    isAvailable: Optional[bool] = True
    time: Optional[int] = 0


class SlotUpdate(SlotBase):
    resource_id: Optional[int] = None
    isAvailable: Optional[bool] = None
    time: Optional[int] = None


class SlotResponse(SlotBase):
    id: int
    resource_id: Optional[int] = None
    isAvailable: Optional[bool] = None
    time: int
