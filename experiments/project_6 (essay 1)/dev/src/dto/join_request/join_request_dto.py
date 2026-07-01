from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class JoinRequestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class JoinRequestCreate(JoinRequestBase):
    requestId: str
    userId: str
    groupId: str
    group_id: int
    groupMembership_id: Optional[int] = None


class JoinRequestUpdate(JoinRequestBase):
    requestId: Optional[str] = None
    userId: Optional[str] = None
    groupId: Optional[str] = None
    group_id: Optional[int] = None
    groupMembership_id: Optional[int] = None


class JoinRequestResponse(JoinRequestBase):
    userId: str
    requestId: str
    userId: str
    groupId: str
    group_id: Optional[int] = None
    groupMembership_id: Optional[int] = None
