from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PatientQueueBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PatientQueueCreate(PatientQueueBase):
    queueId: UUID


class PatientQueueUpdate(PatientQueueBase):
    queueId: Optional[UUID] = None


class PatientQueueResponse(PatientQueueBase):
    id: int
    queueId: UUID
