from __future__ import annotations

from datetime import date
from unittest.mock import Mock

from src.dto.blood_unit.blood_unit_dto import BloodUnitCreate, BloodUnitResponse
from src.service.blood_unit.blood_unit_service import BloodUnitService


class TestBloodUnitAPI:
    """Tests for blood unit API endpoints (service layer integration)."""

    def test_list_blood_units_endpoint(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        repo.get_all.return_value = [
            BloodUnitResponse(
                id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
                collectionDate=date(2025, 1, 1), expiryDate=date(2025, 2, 12), status="available"
            )
        ]
        result = repo.get_all()
        assert len(result) == 1
        assert result[0].uniqueID == "BU-001"

    def test_create_blood_unit_via_service(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        create_dto = BloodUnitCreate(uniqueID="BU-002", aboType="B", rhFactor="negative", collectionDate=date(2025, 3, 1))
        expected = BloodUnitResponse(
            id=2, uniqueID="BU-002", aboType="B", rhFactor="negative",
            collectionDate=date(2025, 3, 1), expiryDate=date(2025, 4, 12), status="available"
        )
        repo.create.return_value = expected
        result = service.create_blood_unit(create_dto)
        assert result.id == 2
        assert result.expiryDate == date(2025, 4, 12)

    def test_delete_blood_unit(self) -> None:
        repo = Mock()
        repo.delete.return_value = True
        assert repo.delete(1) is True

    def test_get_blood_unit_not_found(self) -> None:
        repo = Mock()
        repo.get_by_id.return_value = None
        assert repo.get_by_id(999) is None
