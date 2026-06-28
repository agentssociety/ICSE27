from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class StateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StateCreate(StateBase):
    description: str


class StateUpdate(StateBase):
    description: Optional[str] = None


class StateResponse(StateBase):
    id: int
    description: str
