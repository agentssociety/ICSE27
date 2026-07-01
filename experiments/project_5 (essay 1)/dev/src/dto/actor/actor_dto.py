from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ActorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ActorCreate(ActorBase):
    student_id: int


class ActorUpdate(ActorBase):
    student_id: Optional[int] = None


class ActorResponse(ActorBase):
    id: int
    student_id: Optional[int] = None
