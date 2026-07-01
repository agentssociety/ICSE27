from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BlockRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BlockRecordCreate(BlockRecordBase):
    pass


class BlockRecordUpdate(BlockRecordBase):
    pass


class BlockRecordResponse(BlockRecordBase):
    id: int
    pass
