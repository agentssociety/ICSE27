from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TeacherCreate(TeacherBase):
    name: str


class TeacherUpdate(TeacherBase):
    name: Optional[str] = None


class TeacherResponse(TeacherBase):
    id: int
    name: str
