from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PatientDetailBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientDetailCreate(PatientDetailBase):
    pass


class PatientDetailUpdate(PatientDetailBase):
    pass


class PatientDetailResponse(PatientDetailBase):
    id: int
    pass
