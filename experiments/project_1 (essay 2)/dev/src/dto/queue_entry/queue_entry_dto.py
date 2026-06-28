from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

class QueueEntryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class QueueEntryCreate(QueueEntryBase):
    owner_id: int

class QueueEntryUpdate(QueueEntryBase):
    owner_id: Optional[int] = None

class QueueEntryResponse(QueueEntryBase):
    id: int
    owner_id: Optional[int] = None
