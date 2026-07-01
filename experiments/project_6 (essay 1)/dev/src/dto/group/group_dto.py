from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class GroupBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GroupCreate(GroupBase):
    groupName_id: int
    groupResource_id: int


class GroupUpdate(GroupBase):
    groupName_id: Optional[int] = None
    groupResource_id: Optional[int] = None


class GroupResponse(GroupBase):
    id: int
    groupName_id: Optional[int] = None
    groupResource_id: Optional[int] = None
