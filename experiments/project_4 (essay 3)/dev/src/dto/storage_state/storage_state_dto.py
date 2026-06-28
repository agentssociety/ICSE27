from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class StorageStateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StorageStateCreate(StorageStateBase):
    capacity: int
    used: int


class StorageStateUpdate(StorageStateBase):
    capacity: Optional[int] = None
    used: Optional[int] = None


class StorageStateResponse(StorageStateBase):
    id: int
    capacity: int
    used: int
