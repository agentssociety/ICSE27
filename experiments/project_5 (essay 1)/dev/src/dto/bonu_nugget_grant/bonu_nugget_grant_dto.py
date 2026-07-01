from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BonuNuggetGrantBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BonuNuggetGrantCreate(BonuNuggetGrantBase):
    student_id: int
    instructor_id: Optional[int] = None
    amount: float
    justification: str


class BonuNuggetGrantUpdate(BonuNuggetGrantBase):
    amount: Optional[float] = None
    justification: Optional[str] = None


class BonuNuggetGrantResponse(BonuNuggetGrantBase):
    id: int
    student_id: int
    instructor_id: Optional[int] = None
    amount: float
    justification: str
