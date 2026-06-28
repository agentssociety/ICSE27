from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.dto.emergency_flight import EmergencyRequestDTO, QueueStatusDTO
    from src.repository.emergency_flight import EmergencyHandler, QueueManager

"""
Api layer for the EmergencyFlight domain class

Package: api.emergency_flight
Layer: api
Related tasks: #51
Requirement coverage:
- Handle Emergency Flights
"""

class FlightQueueController:
    def __init__(self, emergencyHandler: EmergencyHandler | None = None, queueManager: QueueManager | None = None) -> None:
        self.emergencyHandler = emergencyHandler
        self.queueManager = queueManager