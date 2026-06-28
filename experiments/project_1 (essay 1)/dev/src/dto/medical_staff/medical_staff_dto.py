from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class MedicalStaffBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MedicalStaffCreate(MedicalStaffBase):
    pass


class MedicalStaffUpdate(MedicalStaffBase):
    pass


class MedicalStaffResponse(MedicalStaffBase):
    id: int
    pass
