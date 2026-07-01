from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BiographyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BiographyCreate(BiographyBase):
    profile_id: int


class BiographyUpdate(BiographyBase):
    profile_id: Optional[int] = None


class BiographyResponse(BiographyBase):
    id: int
    profile_id: Optional[int] = None
