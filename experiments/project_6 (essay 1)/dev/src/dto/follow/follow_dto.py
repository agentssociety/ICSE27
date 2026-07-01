from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class FollowBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FollowCreateDTO(FollowBase):
    followerId: str
    followingId: str


class FollowUpdateDTO(FollowBase):
    state: Optional[str] = None


class FollowResponseDTO(FollowBase):
    id: int
    followerId: str
    followingId: str
    state: str


class FollowRequest(BaseModel):
    initiatorId: str
    targetProfileId: str


class UnfollowRequest(BaseModel):
    initiatorId: str
    targetProfileId: str


class FollowResponse(BaseModel):
    success: bool
    newFollowerCount: int
    message: str
