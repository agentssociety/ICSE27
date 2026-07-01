from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime


"""
Domain layer for the Schedule domain class

Package: domain.schedule
Layer: domain
Related tasks: #107
Requirement coverage:
- Schedule Exams with Date Range and Optional Time Limit
"""


@dataclass
class Schedule:
    exam_id: str
    open_date: datetime
    close_date: datetime
    per_attempt_time_limit_minutes: Optional[int] = None

    def is_accessible(self, current_time: Optional[datetime] = None) -> bool:
        if current_time is None:
            current_time = datetime.now()
        return self.open_date <= current_time <= self.close_date

    def get_time_limit_seconds(self) -> Optional[int]:
        if self.per_attempt_time_limit_minutes is not None:
            return self.per_attempt_time_limit_minutes * 60
        return None


@dataclass
class ScheduleId:
    pass


@dataclass
class ScheduleCreatedEvent:
    pass


@dataclass
class ScheduleUpdatedEvent:
    pass
