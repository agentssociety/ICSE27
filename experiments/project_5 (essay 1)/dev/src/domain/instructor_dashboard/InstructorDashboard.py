from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field

@dataclass
class InstructorDashboard:
    instructor_id: str
    widgets: dict[str, Any] = field(default_factory=dict)

@dataclass
class InstructorDashboardId:
    pass

@dataclass
class InstructorDashboardCreatedEvent:
    pass

@dataclass
class InstructorDashboardUpdatedEvent:
    pass
