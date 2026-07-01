from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field

@dataclass
class CompetencyBreakdown:
    student_id: str
    exam_id: str
    competencies: dict[str, Any] = field(default_factory=dict)

@dataclass
class CompetencyBreakdownId:
    pass

@dataclass
class CompetencyBreakdownCreatedEvent:
    pass

@dataclass
class CompetencyBreakdownUpdatedEvent:
    pass
