from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Reservation domain class

Package: service.reservation
Layer: service
Related tasks: #28
Requirement coverage:
- Automatic Release of Reserved Units for Scheduled Transfusions
"""

class ReservationService(Protocol):
    ...

class ReservationServiceImpl:
    def __init__(self) -> None:
        pass
