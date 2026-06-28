from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TriageNurseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TriageNurseCreate(TriageNurseBase):
    pass


class TriageNurseUpdate(TriageNurseBase):
    pass


class TriageNurseResponse(TriageNurseBase):
    id: int
    pass
