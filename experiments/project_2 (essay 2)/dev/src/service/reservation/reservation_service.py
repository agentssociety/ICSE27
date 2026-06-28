from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from src.dto.reservation.reservation_dto import ReservationCreate, ReservationUpdate, ReservationResponse
from src.dto.blood_unit.blood_unit_dto import BloodUnitUpdate
from src.infra.reservation.reservation_repo_impl import SQLAlchemyReservationRepository
from src.infra.blood_unit.blood_unit_repo_impl import SQLAlchemyBloodUnitRepository


class ReservationService:
    """Service for automated blood unit reservation and release."""

    def __init__(
        self,
        reservation_repo: SQLAlchemyReservationRepository,
        blood_unit_repo: SQLAlchemyBloodUnitRepository,
    ) -> None:
        self._reservation_repo = reservation_repo
        self._blood_unit_repo = blood_unit_repo

    def create_reservation(
        self,
        blood_unit_id: int,
        transfusion_request_id: str,
        request_blood_type: str,
        request_rh_factor: str,
    ) -> Optional[ReservationResponse]:
        """Create a reservation for a blood unit matching a transfusion request.

        Matches by ABO/Rh type. Reservation expires in 24 hours.
        Returns None if the blood unit is not available or type mismatch.
        """
        unit = self._blood_unit_repo.get_by_id(blood_unit_id)
        if unit is None:
            return None
        if unit.status != "available":
            return None
        if unit.aboType != request_blood_type or unit.rhFactor != request_rh_factor:
            return None

        # Mark blood unit as reserved
        self._blood_unit_repo.update(blood_unit_id, BloodUnitUpdate(status="reserved"))

        now = datetime.now()
        expiry = now + timedelta(hours=24)
        create_data = ReservationCreate(
            bloodUnitId=str(blood_unit_id),
            transfusionRequestId=transfusion_request_id,
            bloodUnit_id=blood_unit_id,
        )
        return self._reservation_repo.create(
            create_data,
            reservationTimestamp=now,
            expiryTimestamp=expiry,
            status="active",
        )

    def release_expired_reservations(self) -> int:
        """Release all reservations that have passed their 24-hour expiry.

        Returns the number of released reservations.
        """
        all_reservations = self._reservation_repo.get_all()
        now = datetime.now()
        released_count = 0
        for res in all_reservations:
            if res.status != "active":
                continue
            # Fetch full ORM row to get timestamps
            orm_row = self._reservation_repo.get_orm_by_id(int(res.id))
            if orm_row and now >= orm_row.expiryTimestamp:
                # Release reservation
                self._reservation_repo.update(
                    int(res.id),
                    ReservationUpdate(status="released"),
                )
                # Release blood unit
                self._blood_unit_repo.update(
                    int(orm_row.bloodUnitId),
                    BloodUnitUpdate(status="available"),
                )
                released_count += 1
        return released_count

    def auto_release_all_expired(self) -> int:
        """Convenience wrapper."""
        return self.release_expired_reservations()
