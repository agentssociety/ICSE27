from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduleService:
    def is_exam_accessible(self, open_date: datetime, close_date: datetime, current_time: Optional[datetime] = None) -> bool:
        if current_time is None:
            current_time = datetime.now()
        return open_date <= current_time <= close_date

    def get_time_limit_seconds(self, per_attempt_time_limit_minutes: Optional[int]) -> Optional[int]:
        if per_attempt_time_limit_minutes is not None:
            return per_attempt_time_limit_minutes * 60
        return None
