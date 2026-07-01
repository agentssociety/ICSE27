from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class OperationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass


class OperationResponse(OperationBase):
    id: int
    pass
