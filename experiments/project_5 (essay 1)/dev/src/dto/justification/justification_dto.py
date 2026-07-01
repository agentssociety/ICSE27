from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class JustificationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class JustificationCreate(JustificationBase):
    text: str
    teacherId: str


class JustificationUpdate(JustificationBase):
    text: Optional[str] = None
    teacherId: Optional[str] = None


class JustificationResponse(JustificationBase):
    id: int
    text: str
    teacherId: str
