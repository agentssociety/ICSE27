from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class NuggetWalletBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NuggetWalletCreate(NuggetWalletBase):
    student_id: int
    balance: float = 0.0


class NuggetWalletUpdate(NuggetWalletBase):
    balance: Optional[float] = None


class NuggetWalletResponse(NuggetWalletBase):
    id: int
    student_id: int
    balance: float
