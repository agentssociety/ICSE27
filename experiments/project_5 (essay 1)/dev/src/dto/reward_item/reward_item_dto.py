from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class RewardItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RewardItemCreate(RewardItemBase):
    name: str
    description: Optional[str] = None
    cost: float
    item_type: str = "virtual"
    instructor_id: Optional[int] = None


class RewardItemUpdate(RewardItemBase):
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    item_type: Optional[str] = None


class RewardItemResponse(RewardItemBase):
    id: int
    name: str
    description: Optional[str] = None
    cost: float
    item_type: str
    instructor_id: Optional[int] = None
