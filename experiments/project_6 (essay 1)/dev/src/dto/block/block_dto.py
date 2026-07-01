from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BlockBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BlockCreate(BlockBase):
    pass


class BlockUpdate(BlockBase):
    pass


class BlockResponse(BlockBase):
    id: int
    pass
