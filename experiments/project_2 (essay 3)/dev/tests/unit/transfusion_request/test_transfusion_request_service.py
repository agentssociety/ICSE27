from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import pytest

from src.dto.transfusion_request.transfusion_request_dto import TransfusionRequestCreate, TransfusionRequestUpdate, TransfusionRequestResponse
from src.service.transfusion_request.transfusion_request_service import TransfusionRequestServiceImpl


class TestTransfusionRequestService:
    @pytest.fixture
    def service(self) -> TransfusionRequestServiceImpl:
        repo = MagicMock()
        return TransfusionRequestServiceImpl(repository=repo)

    def test_create_request(self, service: TransfusionRequestServiceImpl) -> None:
        create_data = TransfusionRequestCreate(
            requestId="REQ-001",
            patientId="PAT-001",
            patientABORh="A+",
            bloodType="A+",
            patientID="PAT-001",
        )
        expected_response = TransfusionRequestResponse(
            id="1",
            requestId="REQ-001",
            patientId="PAT-001",
            patientABORh="A+",
            bloodType="A+",
            patientID="PAT-001",
        )
        service._repository.create.return_value = expected_response

        result = service.create_request(create_data)
        assert result == expected_response
        service._repository.create.assert_called_once_with(create_data)

    def test_get_request(self, service: TransfusionRequestServiceImpl) -> None:
        expected = TransfusionRequestResponse(
            id="1",
            requestId="REQ-001",
            patientId="PAT-001",
            patientABORh="A+",
            bloodType="A+",
            patientID="PAT-001",
        )
        service._repository.get_by_id.return_value = expected

        result = service.get_request(1)
        assert result == expected
        service._repository.get_by_id.assert_called_once_with(1)

    def test_list_requests(self, service: TransfusionRequestServiceImpl) -> None:
        expected = [
            TransfusionRequestResponse(
                id="1",
                requestId="REQ-001",
                patientId="PAT-001",
                patientABORh="A+",
                bloodType="A+",
                patientID="PAT-001",
            ),
        ]
        service._repository.get_all.return_value = expected

        result = service.list_requests(skip=0, limit=10)
        assert result == expected
        service._repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_delete_request(self, service: TransfusionRequestServiceImpl) -> None:
        service._repository.delete.return_value = True
        result = service.delete_request(1)
        assert result is True
        service._repository.delete.assert_called_once_with(1)
