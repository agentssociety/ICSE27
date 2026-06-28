from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import Mock

from src.dto.blood_unit.blood_unit_dto import BloodUnitCreate, BloodUnitResponse
from src.service.blood_unit.blood_unit_service import BloodUnitService


class TestBloodUnitService:
    """Unit tests for BloodUnitService."""

    def test_calculate_expiry_date(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        collection_date = date(2025, 1, 1)
        expected = date(2025, 2, 12)
        assert service.calculate_expiry_date(collection_date) == expected

    def test_create_blood_unit_calculates_expiry(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        dto = BloodUnitCreate(uniqueID="BU-001", aboType="A", rhFactor="positive", collectionDate=date(2025, 1, 1))
        expected_expiry = date(2025, 2, 12)
        service.create_blood_unit(dto)
        repo.create.assert_called_once_with(dto, expiryDate=expected_expiry, status="available")

    def test_change_status(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        repo.update.return_value = BloodUnitResponse(
            id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
            collectionDate=date(2025, 1, 1), expiryDate=date(2025, 2, 12), status="issued"
        )
        result = service.change_status(1, "issued")
        assert result is not None
        assert result.status == "issued"
        repo.update.assert_called_once()

    def test_check_and_expire_units(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        expired_unit = BloodUnitResponse(
            id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
            collectionDate=date(2024, 1, 1), expiryDate=date(2024, 2, 12), status="available"
        )
        valid_unit = BloodUnitResponse(
            id=2, uniqueID="BU-002", aboType="B", rhFactor="negative",
            collectionDate=date(2025, 1, 1), expiryDate=date(2099, 2, 12), status="available"
        )
        repo.get_all.return_value = [expired_unit, valid_unit]
        expired_count = service.check_and_expire_units()
        assert expired_count == 1
        assert repo.update.call_count == 1

    def test_get_inventory_summary(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        repo.get_all.return_value = [
            BloodUnitResponse(id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
                              collectionDate=date(2025, 1, 1), expiryDate=date(2025, 2, 12), status="available"),
            BloodUnitResponse(id=2, uniqueID="BU-002", aboType="A", rhFactor="positive",
                              collectionDate=date(2025, 1, 2), expiryDate=date(2025, 2, 13), status="available"),
            BloodUnitResponse(id=3, uniqueID="BU-003", aboType="O", rhFactor="negative",
                              collectionDate=date(2025, 1, 3), expiryDate=date(2025, 2, 14), status="issued"),
        ]
        summary = service.get_inventory_summary()
        assert summary["A/positive"] == 2
        assert "O/negative" not in summary  # issued, not available
        assert "B/positive" not in summary  # no B/positive units

    def test_check_low_stock_alerts_below_threshold(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        repo.get_all.return_value = [
            BloodUnitResponse(id=1, uniqueID="BU-001", aboType="A", rhFactor="positive",
                              collectionDate=date(2025, 1, 1), expiryDate=date(2025, 2, 12), status="available"),
        ]
        alerts = service.check_low_stock_alerts(threshold=5)
        # Should alert with 1 unit for A/positive + alert for all 7 missing types
        a_positive_alert = [a for a in alerts if "A/positive" in a]
        assert len(a_positive_alert) == 1
        assert "only 1 unit" in a_positive_alert[0]
        missing_types_alert = [a for a in alerts if "0 units" in a]
        assert len(missing_types_alert) == 7  # all except A/positive

    def test_check_low_stock_alerts_above_threshold(self) -> None:
        repo = Mock()
        service = BloodUnitService(repo)
        many_units = [
            BloodUnitResponse(id=i, uniqueID=f"BU-{i:03d}", aboType="A", rhFactor="positive",
                              collectionDate=date(2025, 1, 1), expiryDate=date(2025, 2, 12), status="available")
            for i in range(10)
        ]
        repo.get_all.return_value = many_units
        alerts = service.check_low_stock_alerts(threshold=5)
        # A/positive has 10 units, should NOT be alerted
        a_positive_alert = [a for a in alerts if "A/positive" in a and "only" in a]
        assert len(a_positive_alert) == 0
        # But other 7 types are missing
        missing = [a for a in alerts if "0 units" in a]
        assert len(missing) == 7
