from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.emergency_flight import EmergencyFlight, FlightQueue
    from src.domain.flight import Flight
    from src.domain.slot import Slot

"""
Service layer for the EmergencyFlight domain class

Package: service.emergency_flight
Layer: service
Related tasks: #51
Requirement coverage:
- Handle Emergency Flights
"""

class FlightQueueAPI(Protocol):
    ...

class FlightScheduleDatabase(Protocol):
    ...
