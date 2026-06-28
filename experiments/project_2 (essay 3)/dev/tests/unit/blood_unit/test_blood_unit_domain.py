from __future__ import annotations

from datetime import date

import pytest

from src.domain.blood_unit.BloodUnit import BloodUnit


class TestBloodUnitDomain:
    def test_create_blood_unit_valid(self) -> None:
        unit = BloodUnit(abo_rh_type="A+", collection_date=date(2024, 1, 15))
        assert unit.abo_rh_type == "A+"
        assert unit.collection_date == date(2024, 1, 15)
        assert unit.has_complete_data is True
        assert unit.is_expired is False

    def test_create_blood_unit_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="Invalid ABO/Rh type"):
            BloodUnit(abo_rh_type="Invalid", collection_date=date(2024, 1, 15))

    def test_mark_expired(self) -> None:
        unit = BloodUnit(abo_rh_type="O-", collection_date=date(2024, 1, 15))
        assert unit.is_expired is False
        unit.mark_expired()
        assert unit.is_expired is True
