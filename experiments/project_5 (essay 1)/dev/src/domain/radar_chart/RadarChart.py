from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field

@dataclass
class RadarChart:
    competencies: dict[str, int] = field(default_factory=dict)
    studentProfile: Any = None

    def getCompetencies(self) -> dict[str, int]:
        return dict(self.competencies)

    def setCompetency(self, name: str, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError("Competency value must be between 0 and 100")
        self.competencies[name] = value

@dataclass
class RadarChartId:
    pass

@dataclass
class RadarChartCreatedEvent:
    pass

@dataclass
class RadarChartUpdatedEvent:
    pass
