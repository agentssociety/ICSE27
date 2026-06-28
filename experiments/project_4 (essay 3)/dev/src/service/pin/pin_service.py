from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Pin domain class

Package: service.pin
Layer: service
Related tasks: #96
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
"""

class PinService(Protocol):
    ...

class PinServiceImpl:
    def __init__(self) -> None:
        pass
