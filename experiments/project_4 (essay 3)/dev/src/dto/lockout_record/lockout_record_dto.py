from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class LockoutRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LockoutRecordCreate(LockoutRecordBase):
    operation: str


class LockoutRecordUpdate(LockoutRecordBase):
    operation: Optional[str] = None


class LockoutRecordResponse(LockoutRecordBase):
    id: int
    operation: str
