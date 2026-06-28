from __future__ import annotations

from unittest.mock import Mock

from src.dto.transfusion_request.transfusion_request_dto import (
    TransfusionRequestDTO,
    ValidationResult,
    StorageResult,
)
from src.infra.transfusion_request.transfusion_request_repo_impl import (
    SQLAlchemyTransfusionRequestRepository,
)


class TestTransfusionRequestValidation:
    """Tests for transfusion request validation logic."""

    def test_validate_valid_request(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        session = Mock()
        repo._session = session
        dto = TransfusionRequestDTO(bloodType="A", rhFactor="positive", quantity=2)
        result = repo.validate_request(dto)
        assert result.isValid is True
        assert result.errorMessage == ""

    def test_validate_invalid_blood_type(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="X", rhFactor="positive", quantity=2)
        result = repo.validate_request(dto)
        assert result.isValid is False
        assert "blood type" in result.errorMessage.lower()

    def test_validate_invalid_rh_factor(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="A", rhFactor="unknown", quantity=2)
        result = repo.validate_request(dto)
        assert result.isValid is False
        assert "rh factor" in result.errorMessage.lower()

    def test_validate_zero_quantity(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="A", rhFactor="positive", quantity=0)
        result = repo.validate_request(dto)
        assert result.isValid is False
        assert "quantity" in result.errorMessage.lower()

    def test_validate_negative_quantity(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="A", rhFactor="positive", quantity=-1)
        result = repo.validate_request(dto)
        assert result.isValid is False
        assert "quantity" in result.errorMessage.lower()

    def test_store_request_invalid_not_stored(self) -> None:
        """Invalid request should not be stored."""
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="X", rhFactor="positive", quantity=2)
        result = repo.store_request(dto)
        assert result.success is False
        assert result.requestId == ""
        repo._session.add.assert_not_called()
        repo._session.commit.assert_not_called()
