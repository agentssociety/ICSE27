from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class RadarChartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RadarChartCreate(RadarChartBase):
    competencies: dict[str, int]


class RadarChartUpdate(RadarChartBase):
    competencies: Optional[dict[str, int]] = None


class RadarChartResponse(RadarChartBase):
    id: int
    competencies: dict[str, int]
