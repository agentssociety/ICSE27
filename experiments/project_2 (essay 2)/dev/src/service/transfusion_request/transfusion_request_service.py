from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.reservation import Permission

"""
Service layer for the TransfusionRequest domain class

Package: service.transfusion_request
Layer: service
Related tasks: #33, #34, #35, #38
Requirement coverage:
- Accept and Store Transfusion Requests
- Exact ABO/Rh Match First
- Automated Blood Unit Reservation and Release
- Dashboard displaying current stock levels, expiration warnings, and transfusion requests
"""

class BloodBankStaff:
    def __init__(self, permissions: list[Permission] | None = None) -> None:
        self.permissions = permissions

class ClinicalTeams:
    def __init__(self, permissions: list[Permission] | None = None) -> None:
        self.permissions = permissions

class Patients:
    def __init__(self, permissions: list[Permission] | None = None) -> None:
        self.permissions = permissions
