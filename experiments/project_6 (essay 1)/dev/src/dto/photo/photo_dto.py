from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PhotoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PhotoCreate(PhotoBase):
    profile_id: int


class PhotoUpdate(PhotoBase):
    profile_id: Optional[int] = None


class PhotoResponse(PhotoBase):
    id: int
    profile_id: Optional[int] = None
