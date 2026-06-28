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


class TestTransfusionRequestAPI:
    """Tests for transfusion request API layer."""

    def test_submit_valid_request_via_repo(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        session = Mock()
        repo._session = session
        orm_mock = Mock()
        orm_mock.id = 1
        session.add.return_value = None
        session.commit.return_value = None
        session.get.return_value = Mock(
            blood_type="A", rh_factor="positive", units_required=2
        )
        # Override refresh to add id to the passed object
        def refresh_side_effect(obj):
            obj.id = 1
        session.refresh.side_effect = refresh_side_effect

        dto = TransfusionRequestDTO(bloodType="A", rhFactor="positive", quantity=2)
        result = repo.store_request(dto)
        assert result.success is True
        assert result.requestId == "1"

    def test_submit_invalid_request_returns_error(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        dto = TransfusionRequestDTO(bloodType="X", rhFactor="positive", quantity=2)
        result = repo.store_request(dto)
        assert result.success is False
        assert result.requestId == ""

    def test_get_by_id_returns_none_for_missing(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        repo._session.get.return_value = None
        result = repo.get_by_id(999)
        assert result is None

    def test_get_all_returns_list(self) -> None:
        repo = SQLAlchemyTransfusionRequestRepository.__new__(SQLAlchemyTransfusionRequestRepository)
        repo._session = Mock()
        repo._session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        result = repo.get_all()
        assert isinstance(result, list)
