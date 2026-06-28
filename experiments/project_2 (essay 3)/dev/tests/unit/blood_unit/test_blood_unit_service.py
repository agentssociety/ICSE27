from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from src.dto.blood_unit.blood_unit_dto import BloodUnitCreate, BloodUnitUpdate, BloodUnitResponse
from src.service.blood_unit.blood_unit_service import (
    BloodUnitServiceImpl,
    DEFAULT_SHELF_LIFE_DAYS,
    InventoryAlert,
    MIN_INVENTORY_THRESHOLD,
    ABO_RH_COMPATIBILITY,
    DashboardData,
    NearingExpirationUnit,
    NEARING_EXPIRATION_DAYS,
)


class TestBloodUnitService:
    @pytest.fixture
    def service(self) -> BloodUnitServiceImpl:
        repo = MagicMock()
        return BloodUnitServiceImpl(repository=repo)

    def test_create_blood_unit(self, service: BloodUnitServiceImpl) -> None:
        create_data = BloodUnitCreate(abo_rh_type="A+", collection_date=date(2024, 1, 15))
        expected_response = BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15))
        service._repository.create.return_value = expected_response

        result = service.create_blood_unit(create_data)
        assert result == expected_response
        service._repository.create.assert_called_once_with(create_data)

    def test_get_blood_unit(self, service: BloodUnitServiceImpl) -> None:
        expected = BloodUnitResponse(id=1, abo_rh_type="B-", collection_date=date(2024, 1, 15))
        service._repository.get_by_id.return_value = expected

        result = service.get_blood_unit(1)
        assert result == expected
        service._repository.get_by_id.assert_called_once_with(1)

    def test_list_blood_units(self, service: BloodUnitServiceImpl) -> None:
        expected = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15)),
        ]
        service._repository.get_all.return_value = expected

        result = service.list_blood_units(skip=0, limit=10)
        assert result == expected
        service._repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_update_blood_unit(self, service: BloodUnitServiceImpl) -> None:
        update_data = BloodUnitUpdate(abo_rh_type="AB+")
        expected = BloodUnitResponse(id=1, abo_rh_type="AB+", collection_date=date(2024, 1, 15))
        service._repository.update.return_value = expected

        result = service.update_blood_unit(1, update_data)
        assert result == expected
        service._repository.update.assert_called_once_with(1, update_data)

    def test_delete_blood_unit(self, service: BloodUnitServiceImpl) -> None:
        service._repository.delete.return_value = True
        result = service.delete_blood_unit(1)
        assert result is True
        service._repository.delete.assert_called_once_with(1)

    def test_check_expired_units_marks_expired(self, service: BloodUnitServiceImpl) -> None:
        old_date = date.today() - timedelta(days=DEFAULT_SHELF_LIFE_DAYS + 1)
        fresh_date = date.today() - timedelta(days=1)
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=old_date, is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="B-", collection_date=fresh_date, is_expired=False),
        ]
        service._repository.get_all.return_value = units
        service._repository.update.return_value = None

        count = service.check_expired_units()
        assert count == 1
        service._repository.update.assert_called_once_with(1, BloodUnitUpdate(is_expired=True))

    def test_check_expired_units_skips_already_expired(self, service: BloodUnitServiceImpl) -> None:
        old_date = date.today() - timedelta(days=DEFAULT_SHELF_LIFE_DAYS + 1)
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=old_date, is_expired=True),
        ]
        service._repository.get_all.return_value = units

        count = service.check_expired_units()
        assert count == 0
        service._repository.update.assert_not_called()

    def test_check_inventory_raises_alert_when_below_threshold(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=3, abo_rh_type="B-", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        alerts = service.check_inventory_levels()
        assert len(alerts) == 2
        assert any(a.blood_type == "A+" and a.current_count == 2 for a in alerts)
        assert any(a.blood_type == "B-" and a.current_count == 1 for a in alerts)

    def test_check_inventory_no_alert_when_above_threshold(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=i, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False)
            for i in range(MIN_INVENTORY_THRESHOLD + 1)
        ]
        service._repository.get_all.return_value = units

        alerts = service.check_inventory_levels()
        assert len(alerts) == 0

    def test_check_inventory_skips_expired_units(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=True),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        alerts = service.check_inventory_levels()
        assert len(alerts) == 1
        assert alerts[0].current_count == 1

    def test_find_compatible_units_for_O_negative(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="O-", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        compatible = service.find_compatible_units("O-")
        assert len(compatible) == 1
        assert compatible[0].abo_rh_type == "O-"

    def test_find_compatible_units_for_AB_positive(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="O-", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=3, abo_rh_type="B-", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=4, abo_rh_type="AB+", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        compatible = service.find_compatible_units("AB+")
        assert len(compatible) == 4

    def test_find_compatible_units_skips_expired(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="O-", collection_date=date(2024, 1, 15), is_expired=True),
            BloodUnitResponse(id=2, abo_rh_type="O-", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        compatible = service.find_compatible_units("A+")
        assert len(compatible) == 1
        assert compatible[0].id == 2

    def test_find_compatible_units_raises_for_unknown_type(self, service: BloodUnitServiceImpl) -> None:
        with pytest.raises(ValueError, match="Unknown ABO/Rh type"):
            service.find_compatible_units("UnknownType")

    def test_get_dashboard_returns_stock_levels(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
            BloodUnitResponse(id=3, abo_rh_type="B-", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        data = service.get_dashboard_data()
        assert data.stock_levels["A+"] == 2
        assert data.stock_levels["B-"] == 1

    def test_get_dashboard_skips_expired_in_stock(self, service: BloodUnitServiceImpl) -> None:
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=True),
            BloodUnitResponse(id=2, abo_rh_type="A+", collection_date=date(2024, 1, 15), is_expired=False),
        ]
        service._repository.get_all.return_value = units

        data = service.get_dashboard_data()
        assert data.stock_levels["A+"] == 1

    def test_get_dashboard_nearing_expiration(self, service: BloodUnitServiceImpl) -> None:
        today = date.today()
        near_expiry = today - timedelta(days=DEFAULT_SHELF_LIFE_DAYS - NEARING_EXPIRATION_DAYS)
        far_from_expiry = today - timedelta(days=1)
        units = [
            BloodUnitResponse(id=1, abo_rh_type="A+", collection_date=near_expiry, is_expired=False),
            BloodUnitResponse(id=2, abo_rh_type="B-", collection_date=far_from_expiry, is_expired=False),
        ]
        service._repository.get_all.return_value = units

        data = service.get_dashboard_data()
        assert len(data.nearing_expiration) == 1
        assert data.nearing_expiration[0].unit_id == 1
