from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class LikeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LikeCreate(LikeBase):
    pass


class LikeUpdate(LikeBase):
    pass


class LikeResponse(LikeBase):
    id: int
    pass
