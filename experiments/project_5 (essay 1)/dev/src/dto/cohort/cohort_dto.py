from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class CohortBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CohortCreate(CohortBase):
    name: str
    instructor_id: Optional[int] = None


class CohortUpdate(CohortBase):
    name: Optional[str] = None
    instructor_id: Optional[int] = None


class CohortResponse(CohortBase):
    id: int
    name: str
    instructor_id: Optional[int] = None
