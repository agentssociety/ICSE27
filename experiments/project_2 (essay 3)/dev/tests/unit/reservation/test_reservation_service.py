from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.dto.reservation.reservation_dto import ReservationCreate, ReservationUpdate, ReservationResponse
from src.service.reservation.reservation_service import ReservationServiceImpl


class TestReservationService:
    @pytest.fixture
    def service(self) -> ReservationServiceImpl:
        repo = MagicMock()
        return ReservationServiceImpl(repository=repo)

    def test_create_reservation(self, service: ReservationServiceImpl) -> None:
        create_data = ReservationCreate(request_id=1, unit_id=1)
        expected_response = ReservationResponse(id="1-1", request_id=1, unit_id=1)
        service._repository.create.return_value = expected_response

        result = service.create_reservation(create_data)
        assert result == expected_response
        service._repository.create.assert_called_once_with(create_data)

    def test_get_reservation(self, service: ReservationServiceImpl) -> None:
        expected = ReservationResponse(id="1", request_id=1, unit_id=1)
        service._repository.get_by_id.return_value = expected

        result = service.get_reservation(1)
        assert result == expected
        service._repository.get_by_id.assert_called_once_with(1)

    def test_list_reservations(self, service: ReservationServiceImpl) -> None:
        expected = [
            ReservationResponse(id="1", request_id=1, unit_id=1),
        ]
        service._repository.get_all.return_value = expected

        result = service.list_reservations(skip=0, limit=10)
        assert result == expected
        service._repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_release_reservation(self, service: ReservationServiceImpl) -> None:
        existing = ReservationResponse(id="1", request_id=1, unit_id=1)
        service._repository.get_by_id.return_value = existing
        service._repository.update.return_value = existing

        result = service.release_reservation(1)
        assert result == existing
        service._repository.get_by_id.assert_called_once_with(1)
        service._repository.update.assert_called_once_with(1, ReservationUpdate())

    def test_release_reservation_not_found(self, service: ReservationServiceImpl) -> None:
        service._repository.get_by_id.return_value = None

        result = service.release_reservation(999)
        assert result is None
