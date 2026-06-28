from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ActorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ActorCreate(ActorBase):
    name: str


class ActorUpdate(ActorBase):
    name: Optional[str] = None


class ActorResponse(ActorBase):
    id: str
    name: str
