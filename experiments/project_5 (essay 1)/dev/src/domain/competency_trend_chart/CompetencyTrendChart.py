from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class CompetencyTrendChart:
    student_id: str
    competency_id: str
    data_points: list[dict[str, Any]] | None = None

@dataclass
class CompetencyTrendChartId:
    pass

@dataclass
class CompetencyTrendChartCreatedEvent:
    pass

@dataclass
class CompetencyTrendChartUpdatedEvent:
    pass
