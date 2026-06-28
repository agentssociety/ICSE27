from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import Mock

from src.dto.reservation.reservation_dto import ReservationCreate, ReservationResponse
from src.dto.blood_unit.blood_unit_dto import BloodUnitResponse
from src.service.reservation.reservation_service import ReservationService


class TestReservationService:
    """Tests for ReservationService."""

    def test_create_reservation_success(self) -> None:
        blood_repo = Mock()
        res_repo = Mock()
        service = ReservationService(res_repo, blood_repo)

        blood_repo.get_by_id.return_value = BloodUnitResponse(
            id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
            collectionDate=datetime.now().date(), expiryDate=datetime.now().date(),
            status="available"
        )
        res_repo.create.return_value = ReservationResponse(
            id="1", bloodUnitId="1", transfusionRequestId="TR1",
            bloodUnit_id=1, status="active",
        )

        result = service.create_reservation(
            blood_unit_id=1,
            transfusion_request_id="TR1",
            request_blood_type="A",
            request_rh_factor="positive",
        )
        assert result is not None
        assert result.status == "active"
        # Blood unit should have been updated to reserved
        assert blood_repo.update.called
        call_args = blood_repo.update.call_args
        assert call_args[0][0] == 1  # first positional arg is the id
        assert call_args[0][1].status == "reserved"  # second positional arg is BloodUnitUpdate

    def test_create_reservation_blood_unit_not_available(self) -> None:
        blood_repo = Mock()
        res_repo = Mock()
        service = ReservationService(res_repo, blood_repo)

        blood_repo.get_by_id.return_value = BloodUnitResponse(
            id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
            collectionDate=datetime.now().date(), expiryDate=datetime.now().date(),
            status="issued"  # not available
        )
        result = service.create_reservation(1, "TR1", "A", "positive")
        assert result is None
        blood_repo.update.assert_not_called()
        res_repo.create.assert_not_called()

    def test_create_reservation_type_mismatch(self) -> None:
        blood_repo = Mock()
        res_repo = Mock()
        service = ReservationService(res_repo, blood_repo)

        blood_repo.get_by_id.return_value = BloodUnitResponse(
            id=1, uniqueID="BU-001", aboType="B", rhFactor="negative",
            collectionDate=datetime.now().date(), expiryDate=datetime.now().date(),
            status="available"
        )
        result = service.create_reservation(1, "TR1", "A", "positive")
        assert result is None
        blood_repo.update.assert_not_called()
        res_repo.create.assert_not_called()

    def test_release_expired_reservations(self) -> None:
        blood_repo = Mock()
        res_repo = Mock()
        service = ReservationService(res_repo, blood_repo)

        now = datetime.now()
        past = now - timedelta(hours=25)
        # Mock get_all returns active reservation
        res_repo.get_all.return_value = [
            ReservationResponse(id="1", bloodUnitId="1", transfusionRequestId="TR1", bloodUnit_id=1, status="active")
        ]
        # Mock ORM row with past expiry
        orm_mock = Mock()
        orm_mock.id = 1
        orm_mock.bloodUnitId = "1"
        orm_mock.expiryTimestamp = past
        res_repo.get_orm_by_id.return_value = orm_mock

        count = service.release_expired_reservations()
        assert count == 1
        res_repo.update.assert_called()
        blood_repo.update.assert_called()

    def test_no_expired_reservations(self) -> None:
        blood_repo = Mock()
        res_repo = Mock()
        service = ReservationService(res_repo, blood_repo)

        now = datetime.now()
        future = now + timedelta(hours=1)
        res_repo.get_all.return_value = [
            ReservationResponse(id="1", bloodUnitId="1", transfusionRequestId="TR1", bloodUnit_id=1, status="active")
        ]
        orm_mock = Mock()
        orm_mock.expiryTimestamp = future
        res_repo.get_orm_by_id.return_value = orm_mock

        count = service.release_expired_reservations()
        assert count == 0
        res_repo.update.assert_not_called()
        blood_repo.update.assert_not_called()
