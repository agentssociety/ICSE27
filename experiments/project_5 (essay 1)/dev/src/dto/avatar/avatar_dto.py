from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class AvatarBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AvatarCreate(AvatarBase):
    imageUrl: str


class AvatarUpdate(AvatarBase):
    imageUrl: Optional[str] = None


class AvatarResponse(AvatarBase):
    id: int
    imageUrl: str
