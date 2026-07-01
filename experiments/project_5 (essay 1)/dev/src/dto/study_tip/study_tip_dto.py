from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudyTipBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StudyTipCreate(StudyTipBase):
    competency_name: Optional[str] = None
    title: str
    content: Optional[str] = None


class StudyTipUpdate(StudyTipBase):
    competency_name: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


class StudyTipResponse(StudyTipBase):
    id: int
    competency_name: Optional[str] = None
    title: str
    content: Optional[str] = None
