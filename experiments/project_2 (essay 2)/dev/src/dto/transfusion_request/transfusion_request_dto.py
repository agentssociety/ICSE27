from __future__ import annotations

from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.domain.reservation import BloodType
    from src.domain.transfusion_request import RhFactor

"""
Dto layer for the TransfusionRequest domain class

Package: dto.transfusion_request
Layer: dto
Related tasks: #33, #34, #35, #38
Requirement coverage:
- Accept and Store Transfusion Requests
- Exact ABO/Rh Match First
- Automated Blood Unit Reservation and Release
- Dashboard displaying current stock levels, expiration warnings, and transfusion requests
"""

class TransfusionRequestDTO(BaseModel):
    bloodType: str
    rhFactor: str
    quantity: int

class ValidationResult(BaseModel):
    isValid: bool
    errorMessage: str

class StorageResult(BaseModel):
    success: bool
    requestId: str
    errorMessage: str

class Response(BaseModel):
    success: bool
    message: str
    requestId: str
