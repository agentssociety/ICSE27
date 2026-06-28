from __future__ import annotations

from typing import Any

"""
Service layer for the TransfusionRequest domain class

Package: service.transfusion_request
Layer: service
Related tasks: #26, #27, #31
Requirement coverage:
- Accept and Log Transfusion Requests
- Blood Unit Compatibility Matching
- Inventory Dashboard Display
"""

class HealthcareProvider:
    def __init__(self, name: str | None = None, credentials: str | None = None) -> None:
        self.name = name
        self.credentials = credentials

class BloodBankTechnician:
    def __init__(self, name: str | None = None, credentials: str | None = None) -> None:
        self.name = name
        self.credentials = credentials

class IT_Team:
    def __init__(self, teamName: str | None = None) -> None:
        self.teamName = teamName
