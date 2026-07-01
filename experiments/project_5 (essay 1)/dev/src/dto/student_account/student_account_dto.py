from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class StudentAccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StudentAccountCreate(StudentAccountBase):
    registrationData_id: int


class StudentAccountUpdate(StudentAccountBase):
    registrationData_id: Optional[int] = None


class StudentAccountResponse(StudentAccountBase):
    id: int
    registrationData_id: Optional[int] = None
