from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Card domain class

Package: service.card
Layer: service
Related tasks: #96
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
"""

class CardService(Protocol):
    ...

class CardServiceImpl:
    def __init__(self) -> None:
        pass
