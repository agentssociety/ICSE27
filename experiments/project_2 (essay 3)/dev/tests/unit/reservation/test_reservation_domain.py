from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from src.domain.reservation.Reservation import Reservation, ReservationStatus


class TestReservationDomain:
    def test_create_reservation(self) -> None:
        now = datetime(2024, 1, 15, 10, 0, 0)
        reservation = Reservation(
            id="RES-001",
            request_id="REQ-001",
            unit_id=1,
            reserved_at=now,
        )
        assert reservation.id == "RES-001"
        assert reservation.request_id == "REQ-001"
        assert reservation.unit_id == 1
        assert reservation.status == ReservationStatus.ACTIVE

    def test_is_expired_returns_false_for_recent(self) -> None:
        now = datetime(2024, 1, 15, 10, 0, 0)
        reservation = Reservation(
            id="RES-001",
            request_id="REQ-001",
            unit_id=1,
            reserved_at=now,
            timeout_minutes=30,
        )
        later = now + timedelta(minutes=15)
        assert reservation.is_expired(later) is False

    def test_is_expired_returns_true_after_timeout(self) -> None:
        now = datetime(2024, 1, 15, 10, 0, 0)
        reservation = Reservation(
            id="RES-001",
            request_id="REQ-001",
            unit_id=1,
            reserved_at=now,
            timeout_minutes=30,
        )
        later = now + timedelta(minutes=31)
        assert reservation.is_expired(later) is True

    def test_release(self) -> None:
        now = datetime(2024, 1, 15, 10, 0, 0)
        reservation = Reservation(
            id="RES-001",
            request_id="REQ-001",
            unit_id=1,
            reserved_at=now,
        )
        reservation.release()
        assert reservation.status == ReservationStatus.RELEASED

    def test_expire(self) -> None:
        now = datetime(2024, 1, 15, 10, 0, 0)
        reservation = Reservation(
            id="RES-001",
            request_id="REQ-001",
            unit_id=1,
            reserved_at=now,
        )
        reservation.expire()
        assert reservation.status == ReservationStatus.EXPIRED
