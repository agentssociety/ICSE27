from __future__ import annotations

from datetime import datetime
from typing import Optional, Protocol

from src.domain.reservation.Reservation import Reservation, ReservationStatus
from src.dto.reservation.reservation_dto import ReservationCreate, ReservationUpdate, ReservationResponse
from src.repository.reservation.reservation_repository import ReservationRepository


class ReservationService(Protocol):
    """Protocol for reservation service operations."""

    def create_reservation(self, data: ReservationCreate) -> ReservationResponse:
        """Create a new reservation."""
        ...

    def get_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        """Get a reservation by ID."""
        ...

    def list_reservations(self, skip: int = 0, limit: int = 100) -> list[ReservationResponse]:
        """List all reservations."""
        ...

    def release_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        """Release a reservation."""
        ...

    def release_expired_reservations(self) -> int:
        """Release all expired reservations. Returns count of released reservations."""
        ...


class ReservationServiceImpl:
    """Service implementation for reservation operations."""

    def __init__(self, repository: ReservationRepository) -> None:
        self._repository = repository

    def create_reservation(self, data: ReservationCreate) -> ReservationResponse:
        domain = Reservation(
            id=str(data.request_id) + "-" + str(data.unit_id),
            request_id=str(data.request_id),
            unit_id=data.unit_id,
            reserved_at=datetime.now(),
        )
        return self._repository.create(data)

    def get_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        return self._repository.get_by_id(reservation_id)

    def list_reservations(self, skip: int = 0, limit: int = 100) -> list[ReservationResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def release_reservation(self, reservation_id: int) -> Optional[ReservationResponse]:
        reservation = self._repository.get_by_id(reservation_id)
        if reservation is None:
            return None
        update_data = ReservationUpdate()
        return self._repository.update(reservation_id, update_data)

    def release_expired_reservations(self) -> int:
        """Release all expired reservations."""
        reservations = self._repository.get_all(skip=0, limit=10000)
        now = datetime.now()
        released_count = 0
        for reservation in reservations:
            domain = Reservation(
                id=reservation.id,
                request_id=str(reservation.request_id) if reservation.request_id else "",
                unit_id=reservation.unit_id if reservation.unit_id else 0,
                reserved_at=datetime.now(),
            )
            if domain.is_expired(now):
                update_data = ReservationUpdate()
                self._repository.update(int(reservation.id), update_data)
                released_count += 1
        return released_count

