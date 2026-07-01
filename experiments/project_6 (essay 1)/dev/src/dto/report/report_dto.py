from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReportCreate(ReportBase):
    pass


class ReportUpdate(ReportBase):
    pass


class ReportResponse(ReportBase):
    id: int
    pass
