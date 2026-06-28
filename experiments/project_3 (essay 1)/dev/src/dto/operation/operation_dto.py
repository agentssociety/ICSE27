from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class OperationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OperationCreate(OperationBase):
    initiator_id: int
    grant_id: int
    pre_id: int
    post_id: int


class OperationUpdate(OperationBase):
    initiator_id: Optional[int] = None
    grant_id: Optional[int] = None
    pre_id: Optional[int] = None
    post_id: Optional[int] = None


class OperationResponse(OperationBase):
    id: int
    initiator_id: Optional[int] = None
    grant_id: Optional[int] = None
    pre_id: Optional[int] = None
    post_id: Optional[int] = None
