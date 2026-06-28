from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class HealthcareFacilityManagementBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthcareFacilityManagementCreate(HealthcareFacilityManagementBase):
    pass


class HealthcareFacilityManagementUpdate(HealthcareFacilityManagementBase):
    pass


class HealthcareFacilityManagementResponse(HealthcareFacilityManagementBase):
    id: int
    pass
