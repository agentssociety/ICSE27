from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PatientCareTeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientCareTeamCreate(PatientCareTeamBase):
    pass


class PatientCareTeamUpdate(PatientCareTeamBase):
    pass


class PatientCareTeamResponse(PatientCareTeamBase):
    id: int
    pass
