from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CompetencyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompetencyCreate(CompetencyBase):
    name: str


class CompetencyUpdate(CompetencyBase):
    name: Optional[str] = None


class CompetencyResponse(CompetencyBase):
    id: int
    name: str
