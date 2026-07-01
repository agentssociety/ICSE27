from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScheduleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ScheduleCreateRequest(ScheduleBase):
    exam_id: str
    open_date: datetime
    close_date: datetime
    per_attempt_time_limit_minutes: Optional[int] = None


class ScheduleUpdateRequest(ScheduleBase):
    open_date: Optional[datetime] = None
    close_date: Optional[datetime] = None
    per_attempt_time_limit_minutes: Optional[int] = None


class ScheduleResponse(ScheduleBase):
    id: int
    exam_id: str
    open_date: datetime
    close_date: datetime
    per_attempt_time_limit_minutes: Optional[int] = None
