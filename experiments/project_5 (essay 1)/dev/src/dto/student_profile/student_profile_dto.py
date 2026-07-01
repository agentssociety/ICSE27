from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StudentProfileCreate(StudentProfileBase):
    student_id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class StudentProfileUpdate(StudentProfileBase):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class StudentProfileResponse(StudentProfileBase):
    id: int
    student_id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
