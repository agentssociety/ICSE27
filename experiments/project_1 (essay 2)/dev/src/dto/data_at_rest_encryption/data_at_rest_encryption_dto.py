from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

class DataAtRestEncryptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class DataAtRestEncryptionCreate(DataAtRestEncryptionBase):
    resource_id: int
    encrypted: bool

class DataAtRestEncryptionUpdate(DataAtRestEncryptionBase):
    resource_id: Optional[int] = None
    encrypted: Optional[bool] = None

class DataAtRestEncryptionResponse(DataAtRestEncryptionBase):
    id: int
    resource_id: Optional[int] = None
    encrypted: bool
