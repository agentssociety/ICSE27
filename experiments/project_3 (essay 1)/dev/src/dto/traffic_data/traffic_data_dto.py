from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

# Removed import that causes ModuleNotFoundError


class TrafficDataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TrafficDataCreate(TrafficDataBase):
    runwayLoads: dict[Any, int]


class TrafficDataUpdate(TrafficDataBase):
    runwayLoads: Optional[dict[Any, int]] = None


class TrafficDataResponse(TrafficDataBase):
    id: int
    runwayLoads: dict[Any, int]