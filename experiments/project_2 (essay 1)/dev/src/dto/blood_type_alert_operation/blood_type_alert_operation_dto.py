from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BloodTypeAlertOperationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BloodTypeAlertOperationCreate(BloodTypeAlertOperationBase):
    pass


class BloodTypeAlertOperationUpdate(BloodTypeAlertOperationBase):
    pass


class BloodTypeAlertOperationResponse(BloodTypeAlertOperationBase):
    id: int
    pass
