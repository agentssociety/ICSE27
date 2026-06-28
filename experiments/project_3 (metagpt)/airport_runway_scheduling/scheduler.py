"""Core scheduling logic for the flight scheduling system.

This module implements the Scheduler class that manages runways,
flight queues, and slot allocation with priority and emergency handling.
It enforces a 3-minute separation gap between consecutive slots on the same runway.
"""

from __future__ import annotations

import datetime
import heapq
from typing import Dict, List, Optional

from models import Flight, Slot, Runway


class Scheduler:
    """Manages runway scheduling, flight allocation, and emergency handling."""

    # Minimum gap between consecutive slots on the same runway (in minutes)
    SLOT_GAP_MINUTES = 3
    # Maximum time window for reassignment (in minutes)
    REASSIGNMENT_WINDOW_MINUTES = 60

    def __init__(self) -> None:
        """Initialize the scheduler with two runways and empty queues."""
        self.runways: Dict[int, Runway] = {
            1: Runway(1),
            2: Runway(2),
        }
        self.flight_queue: List[Flight] = []
        self.emergency_queue: List[Flight] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_flight(self, flight: Flight) -> bool:
        """Register a new flight and attempt to allocate a slot.

        Args:
            flight: The flight to register.

        Returns:
            True if the flight was successfully registered and allocated.
        """
        if flight.is_emergency:
            self.emergency_queue.append(flight)
            return self.handle_emergency(flight) is not None
        else:
            heapq.heappush(self.flight_queue, flight)
            return self.allocate_slot(flight) is not None

    def allocate_slot(self, flight: Flight) -> Optional[Slot]:
        """Allocate the best available slot for a flight.

        Uses arrival priority: arrivals get preference over departures.
        Finds the earliest slot across both runways while respecting the
        3-minute separation gap.

        Args:
            flight: The flight to allocate.

        Returns:
            The allocated Slot, or None if allocation failed.
        """
        best_slot: Optional[Slot] = None
        best_runway: Optional[int] = None

        for runway_id, runway in self.runways.items():
            if not runway.is_open:
                continue
            slot = self._find_next_slot_with_gap(runway, flight.estimated_time)
            if slot is None:
                continue

            # Compare with current best
            if best_slot is None:
                best_slot = slot
                best_runway = runway_id
            elif slot.start_time < best_slot.start_time:
                best_slot = slot
                best_runway = runway_id
            # For equal times, prefer arrivals on runway 1
            elif (slot.start_time == best_slot.start_time
                  and flight.flight_type == "arrival"
                  and runway_id == 1):
                best_slot = slot
                best_runway = runway_id

        if best_slot is None:
            return None

        best_slot.assign_flight(flight)
        return best_slot

    def handle_emergency(self, flight: Flight) -> Optional[Slot]:
        """Handle an emergency flight by finding the earliest possible slot.

        Emergency flights get priority over all other flights.
        May displace existing flights if necessary across both runways.

        Args:
            flight: The emergency flight to handle.

        Returns:
            The emergency slot, or None if no slot available.
        """
        # Find earliest slot across both runways (emergencies ignore gap)
        earliest_slot: Optional[Slot] = None
        earliest_runway: Optional[int] = None
        for runway_id, runway in self.runways.items():
            if not runway.is_open:
                continue
            # Emergency directly uses get_next_available_slot (no gap enforcement)
            slot = runway.get_next_available_slot(flight.estimated_time)
            if slot is None:
                continue
            if earliest_slot is None or slot.start_time < earliest_slot.start_time:
                earliest_slot = slot
                earliest_runway = runway_id

        if earliest_slot is None:
            return None

        # Assign the emergency flight
        earliest_slot.assign_flight(flight)

        # Displace conflicting flights on both runways (in case of overlap)
        displaced_flights: List[Flight] = []
        for runway_id, runway in self.runways.items():
            if runway.is_open:
                displaced = self._displace_flights(earliest_slot, runway_id)
                displaced_flights.extend(displaced)

        if displaced_flights:
            self._re_queue_flights(displaced_flights)

        return earliest_slot

    def close_runway(self, runway_id: int) -> List[Flight]:
        """Close a runway and reassign all future flights.

        Args:
            runway_id: The runway to close (1 or 2).

        Returns:
            List of flights that were delayed due to reassignment.

        Raises:
            ValueError: If the runway does not exist or is already closed.
        """
        if runway_id not in self.runways:
            raise ValueError(f"Runway {runway_id} does not exist")

        runway = self.runways[runway_id]
        if not runway.is_open:
            raise ValueError(f"Runway {runway_id} is already closed")

        # Close the runway
        runway.close()

        # Get all future flights on this runway
        now = datetime.datetime.now()
        future_flights: List[Flight] = []
        for slot in runway.slots:
            if slot.flight is not None and slot.start_time > now:
                future_flights.append(slot.flight)
                slot.release()  # This clears the flight's assigned_slot

        # Reassign flights to the other runway with gap enforcement
        delayed_flights: List[Flight] = []
        other_runway_id = 2 if runway_id == 1 else 1
        other_runway = self.runways[other_runway_id]

        for flight in future_flights:
            # Use _find_next_slot_with_gap to respect gap on other runway
            new_slot = self._find_next_slot_with_gap(
                other_runway, flight.estimated_time
            )
            if new_slot is not None:
                time_diff = (
                    new_slot.start_time - flight.estimated_time
                ).total_seconds() / 60
                if abs(time_diff) <= self.REASSIGNMENT_WINDOW_MINUTES:
                    new_slot.assign_flight(flight)
                else:
                    flight.mark_delayed()
                    delayed_flights.append(flight)
                    # Still assign to the earliest available slot (may exceed window)
                    new_slot.assign_flight(flight)
            else:
                flight.mark_delayed()
                delayed_flights.append(flight)

        return delayed_flights

    def reassign_flights(self, flights: List[Flight]) -> None:
        """Reassign a list of flights to available slots.

        Args:
            flights: List of flights to reassign.
        """
        for flight in flights:
            self.allocate_slot(flight)

    def get_timetable(self, runway_id: int) -> List[Slot]:
        """Get the timetable for a specific runway.

        Args:
            runway_id: The runway to get the timetable for.

        Returns:
            List of slots for the specified runway, sorted by time.

        Raises:
            ValueError: If the runway does not exist.
        """
        if runway_id not in self.runways:
            raise ValueError(f"Runway {runway_id} does not exist")

        runway = self.runways[runway_id]
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        return runway.get_slots_in_range(now, tomorrow)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_next_slot_with_gap(
        self, runway: Runway, after_time: datetime.datetime
    ) -> Optional[Slot]:
        """Find the next available slot on a runway that respects the
        3‑minute gap from the last occupied slot.

        This method wraps the runway's get_next_available_slot but ensures
        that the slot's start time is at least SLOT_GAP_MINUTES after the
        end time of the previous occupied slot on the same runway.

        Args:
            runway: The runway to search.
            after_time: The earliest acceptable start time.

        Returns:
            The first available Slot that satisfies the gap, or None.
        """
        if not runway.is_open:
            return None

        # Sort slots by start time
        sorted_slots = sorted(runway.slots, key=lambda s: s.start_time)

        # Find the last occupied slot that ends before after_time
        last_end: Optional[datetime.datetime] = None
        for slot in sorted_slots:
            if slot.flight is not None and slot.end_time <= after_time:
                last_end = slot.end_time

        # Calculate the earliest start time respecting the gap
        if last_end is not None:
            min_start = last_end + datetime.timedelta(minutes=self.SLOT_GAP_MINUTES)
        else:
            min_start = after_time

        # Get the next available slot from the runway
        return runway.get_next_available_slot(min_start)

    def _displace_flights(
        self, emergency_slot: Slot, runway_id: int
    ) -> List[Flight]:
        """Displace flights that conflict with an emergency slot on a
        specific runway.

        Only slots on the given runway are considered, and only those that
        overlap with the emergency slot are displaced.

        Args:
            emergency_slot: The emergency slot that may cause displacement.
            runway_id: The runway where the emergency slot is located.

        Returns:
            List of displaced flights (already marked delayed).
        """
        displaced: List[Flight] = []
        runway = self.runways[runway_id]
        for slot in runway.slots:
            if slot.flight is None:
                continue
            # Check overlap (start before em end, end after em start)
            if (
                slot.start_time < emergency_slot.end_time
                and slot.end_time > emergency_slot.start_time
            ):
                flight = slot.flight
                slot.release()
                flight.mark_delayed()
                displaced.append(flight)
        return displaced

    def _re_queue_flights(self, flights: List[Flight]) -> None:
        """Re-queue displaced flights for re-allocation.

        Flights are re-allocated based on their original estimated times,
        maintaining arrival priority over departures.  If no slot is
        available, they remain in the normal queue as delayed.

        Args:
            flights: List of displaced flights to re-queue.
        """
        for flight in flights:
            new_slot = self.allocate_slot(flight)
            if new_slot is None:
                # Keep as delayed and push back onto queue
                flight.mark_delayed()
                heapq.heappush(self.flight_queue, flight)

    def __repr__(self) -> str:
        return (
            f"Scheduler(runways={list(self.runways.keys())}, "
            f"queue_size={len(self.flight_queue)}, "
            f"emergencies={len(self.emergency_queue)})"
        )
