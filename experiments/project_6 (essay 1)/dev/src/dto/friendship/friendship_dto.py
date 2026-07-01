from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class FriendshipBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FriendshipCreate(FriendshipBase):
    abstract_isMutual: bool


class FriendshipUpdate(FriendshipBase):
    abstract_isMutual: Optional[bool] = None


class FriendshipResponse(FriendshipBase):
    id: int
    abstract_isMutual: bool
