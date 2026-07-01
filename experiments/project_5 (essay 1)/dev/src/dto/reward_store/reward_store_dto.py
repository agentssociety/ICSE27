from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class RewardStoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RewardStoreCreate(RewardStoreBase):
    name: str
    instructor_id: Optional[int] = None


class RewardStoreUpdate(RewardStoreBase):
    name: Optional[str] = None
    instructor_id: Optional[int] = None


class RewardStoreResponse(RewardStoreBase):
    id: int
    name: str
    instructor_id: Optional[int] = None
