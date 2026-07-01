from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StudentCreate(StudentBase):
    name: str
    email: str
    avatar_url: Optional[str] = None


class StudentUpdate(StudentBase):
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None
