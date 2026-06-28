from __future__ import annotations

from datetime import datetime, timedelta

from src.domain.reservation.Reservation import (
    Reservation,
    ReservationStatus,
    BloodUnitStatus,
    TransfusionRequestStatus,
    BloodType,
    Role,
    Permission,
)


class TestReservationDomain:
    """Unit tests for Reservation domain objects."""

    def test_reservation_creation(self) -> None:
        future_now = datetime.now() + timedelta(hours=1)
        expiry = future_now + timedelta(hours=24)
        res = Reservation(
            id="R001",
            bloodUnitId="BU001",
            transfusionRequestId="TR001",
            reservationTimestamp=future_now,
            expiryTimestamp=expiry,
            status=ReservationStatus.ACTIVE,
        )
        assert res.id == "R001"
        assert res.status == ReservationStatus.ACTIVE
        assert res.is_expired() is False  # future expiry

    def test_release_reservation(self) -> None:
        now = datetime.now()
        expiry = now + timedelta(hours=24)
        res = Reservation(
            id="R001", bloodUnitId="BU001", transfusionRequestId="TR001",
            reservationTimestamp=now, expiryTimestamp=expiry,
            status=ReservationStatus.ACTIVE,
        )
        res.release()
        assert res.status == ReservationStatus.RELEASED

    def test_issue_reservation(self) -> None:
        now = datetime.now()
        expiry = now + timedelta(hours=24)
        res = Reservation(
            id="R001", bloodUnitId="BU001", transfusionRequestId="TR001",
            reservationTimestamp=now, expiryTimestamp=expiry,
            status=ReservationStatus.ACTIVE,
        )
        res.issue()
        assert res.status == ReservationStatus.ISSUED

    def test_is_expired_past_expiry(self) -> None:
        now = datetime.now()
        past = now - timedelta(hours=1)
        expiry = now - timedelta(minutes=1)
        res = Reservation(
            id="R001", bloodUnitId="BU001", transfusionRequestId="TR001",
            reservationTimestamp=past, expiryTimestamp=expiry,
            status=ReservationStatus.ACTIVE,
        )
        assert res.is_expired() is True

    def test_enum_values(self) -> None:
        assert ReservationStatus.ACTIVE.value == "active"
        assert ReservationStatus.RELEASED.value == "released"
        assert ReservationStatus.ISSUED.value == "issued"
        assert BloodUnitStatus.RESERVED.value == "reserved"
