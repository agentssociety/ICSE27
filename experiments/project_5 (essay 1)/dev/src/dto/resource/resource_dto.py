from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ResourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ResourceCreate(ResourceBase):
    owner_id: int


class ResourceUpdate(ResourceBase):
    owner_id: Optional[int] = None


class ResourceResponse(ResourceBase):
    id: int
    owner_id: Optional[int] = None
