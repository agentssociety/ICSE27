from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class GroupMembershipBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GroupMembershipCreate(GroupMembershipBase):
    groupId: str
    userId: str
    group_id: int


class GroupMembershipUpdate(GroupMembershipBase):
    groupId: Optional[str] = None
    userId: Optional[str] = None
    group_id: Optional[int] = None


class GroupMembershipResponse(GroupMembershipBase):
    userId: str
    groupId: str
    userId: str
    group_id: Optional[int] = None
