from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field

@dataclass
class CohortLeaderboard:
    cohort_id: str
    rankings: list[dict[str, Any]] = field(default_factory=list)  # list of {student_id, score}

@dataclass
class CohortLeaderboardId:
    pass

@dataclass
class CohortLeaderboardCreatedEvent:
    pass

@dataclass
class CohortLeaderboardUpdatedEvent:
    pass
