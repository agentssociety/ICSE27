from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class DifficultyTagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DifficultyTagCreate(DifficultyTagBase):
    resource_id: int


class DifficultyTagUpdate(DifficultyTagBase):
    resource_id: Optional[int] = None


class DifficultyTagResponse(DifficultyTagBase):
    id: int
    resource_id: Optional[int] = None
