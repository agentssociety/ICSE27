from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class RegistrationDataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RegistrationDataCreate(RegistrationDataBase):
    name: str
    email: str
    password: str


class RegistrationDataUpdate(RegistrationDataBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class RegistrationDataResponse(RegistrationDataBase):
    id: int
    name: str
    email: str
    password: str
