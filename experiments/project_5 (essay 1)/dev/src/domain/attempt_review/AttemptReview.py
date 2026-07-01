from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class AttemptReview:
    student_id: str
    exam_id: str
    score: float = 0.0
    feedback: str = ""
    reviewed_at: str = ""

@dataclass
class AttemptReviewId:
    pass

@dataclass
class AttemptReviewCreatedEvent:
    pass

@dataclass
class AttemptReviewUpdatedEvent:
    pass
