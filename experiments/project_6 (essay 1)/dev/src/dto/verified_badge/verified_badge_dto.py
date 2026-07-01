from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class VerifiedBadgeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VerifiedBadgeCreate(VerifiedBadgeBase):
    pass


class VerifiedBadgeUpdate(VerifiedBadgeBase):
    pass


class VerifiedBadgeResponse(VerifiedBadgeBase):
    id: int
    pass
