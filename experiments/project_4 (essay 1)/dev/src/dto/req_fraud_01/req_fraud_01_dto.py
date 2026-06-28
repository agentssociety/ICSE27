from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class REQ_FRAUD_01Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class REQ_FRAUD_01Create(REQ_FRAUD_01Base):
    initiator_id: int
    target_id: int
    channel_id: int
    pre_id: int
    post_id: int


class REQ_FRAUD_01Update(REQ_FRAUD_01Base):
    initiator_id: Optional[int] = None
    target_id: Optional[int] = None
    channel_id: Optional[int] = None
    pre_id: Optional[int] = None
    post_id: Optional[int] = None


class REQ_FRAUD_01Response(REQ_FRAUD_01Base):
    id: int
    initiator_id: Optional[int] = None
    target_id: Optional[int] = None
    channel_id: Optional[int] = None
    pre_id: Optional[int] = None
    post_id: Optional[int] = None
