from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ChartPointBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ChartPointCreate(ChartPointBase):
    value: float
    label: str


class ChartPointUpdate(ChartPointBase):
    value: Optional[float] = None
    label: Optional[str] = None


class ChartPointResponse(ChartPointBase):
    id: int
    value: float
    label: str
