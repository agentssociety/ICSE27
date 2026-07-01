from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BadgeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BadgeCreate(BadgeBase):
    name: str
    description: str
    student_id: Optional[int] = None


class BadgeUpdate(BadgeBase):
    name: Optional[str] = None
    description: Optional[str] = None
    student_id: Optional[int] = None


class BadgeResponse(BadgeBase):
    id: int
    name: str
    description: str
    student_id: Optional[int] = None
