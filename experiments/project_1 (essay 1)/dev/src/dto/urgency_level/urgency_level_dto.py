from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class UrgencyLevelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UrgencyLevelCreateRequest(UrgencyLevelBase):
    level: str
    sort_order: int


class UrgencyLevelUpdateRequest(UrgencyLevelBase):
    level: Optional[str] = None
    sort_order: Optional[int] = None


class UrgencyLevelResponse(UrgencyLevelBase):
    id: int
    level: str
    sort_order: int
