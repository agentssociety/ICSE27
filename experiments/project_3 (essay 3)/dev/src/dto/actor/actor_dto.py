from __future__ import annotations


from pydantic import BaseModel, ConfigDict


class ActorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ActorCreate(ActorBase):
    pass


class ActorUpdate(ActorBase):
    pass


class ActorResponse(ActorBase):
    id: int
    pass
