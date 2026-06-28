from __future__ import annotations


from pydantic import BaseModel, ConfigDict


class ResourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    pass


class ResourceResponse(ResourceBase):
    id: int
    pass
