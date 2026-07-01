from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    pass
