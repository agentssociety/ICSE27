from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class IT_TeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IT_TeamCreate(IT_TeamBase):
    pass


class IT_TeamUpdate(IT_TeamBase):
    pass


class IT_TeamResponse(IT_TeamBase):
    id: int
