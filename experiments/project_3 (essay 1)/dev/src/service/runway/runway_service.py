from __future__ import annotations

from typing import Any

"""
Service layer for the Runway domain class

Package: service.runway
Layer: service
Related tasks: #50, #52
Requirement coverage:
- Automatic Reassignment of Flights During Runway Closure
- View Runway Slot Timetable
"""

class System:
    def __init__(self) -> None:
        self._flights: list[Any] = []
        self._runways: list[Any] = []
        self._assignments: dict[Any, Any] = {}

    def rerouteToExternalAirport(self, flight: Any) -> None:
        """Reroute a flight to an external airport when runway is closed."""
        if flight in self._flights:
            self._flights.remove(flight)
        if flight in self._assignments:
            del self._assignments[flight]

    def holdFlightUntilAvailable(self, flight: Any) -> None:
        """Hold a flight in queue until a runway becomes available."""
        if flight not in self._flights:
            self._flights.append(flight)

    def solveComplexConstraints(self, flights: Any, availableRunways: Any) -> Any:
        """Solve complex constraint satisfaction for flight-to-runway assignment."""
        if not flights or not availableRunways:
            return {}
        # Simple implementation: assign flights to first available runway
        result = {}
        if hasattr(flights, '__iter__'):
            flight_list = list(flights)
        else:
            flight_list = [flights]

        if hasattr(availableRunways, '__iter__'):
            runway_list = list(availableRunways)
        else:
            runway_list = [availableRunways]

        for i, flight in enumerate(flight_list):
            runway_idx = i % len(runway_list)
            result[flight] = runway_list[runway_idx]
            self._assignments[flight] = runway_list[runway_idx]
        return result

    def updateAllAssignments(self) -> None:
        """Update all current assignments (placeholder for actual DB sync logic)."""
        pass
