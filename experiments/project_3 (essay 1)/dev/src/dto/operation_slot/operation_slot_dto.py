from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class OperationSlotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OperationSlotCreate(OperationSlotBase):
    op_id: int
    slot_id: int


class OperationSlotUpdate(OperationSlotBase):
    op_id: Optional[int] = None
    slot_id: Optional[int] = None


class OperationSlotResponse(OperationSlotBase):
    id: int
    op_id: Optional[int] = None
    slot_id: Optional[int] = None
