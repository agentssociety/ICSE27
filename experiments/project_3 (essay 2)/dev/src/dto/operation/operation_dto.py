from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class OperationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OperationCreate(OperationBase):
    description: str


class OperationUpdate(OperationBase):
    description: Optional[str] = None


class OperationResponse(OperationBase):
    id: int
    description: str
