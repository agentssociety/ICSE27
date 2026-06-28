from __future__ import annotations

from datetime import date, timedelta
from src.domain.blood_unit.BloodUnit import (
    ABOType, RhFactor, BloodUnitStatus, BloodUnit, Permission, Actor
)


class TestBloodUnitDomain:
    """Unit tests for BloodUnit domain objects."""

    def test_abo_type_enum_values(self) -> None:
        assert ABOType.A.value == "a"
        assert ABOType.B.value == "b"
        assert ABOType.AB.value == "ab"
        assert ABOType.O.value == "o"

    def test_rh_factor_enum_values(self) -> None:
        assert RhFactor.POSITIVE.value == "positive"
        assert RhFactor.NEGATIVE.value == "negative"

    def test_blood_unit_status_enum_values(self) -> None:
        assert BloodUnitStatus.AVAILABLE.value == "available"
        assert BloodUnitStatus.ISSUED.value == "issued"
        assert BloodUnitStatus.EXPIRED.value == "expired"

    def test_blood_unit_dataclass_creation(self) -> None:
        unit = BloodUnit(
            uniqueID="BU-001",
            aboType=ABOType.A,
            rhFactor=RhFactor.POSITIVE,
            collectionDate=date(2025, 1, 1),
            expiryDate=date(2025, 2, 12),
            status=BloodUnitStatus.AVAILABLE,
        )
        assert unit.uniqueID == "BU-001"
        assert unit.aboType == ABOType.A
        assert unit.rhFactor == RhFactor.POSITIVE
        assert unit.collectionDate == date(2025, 1, 1)
        assert unit.expiryDate == date(2025, 1, 1) + timedelta(days=42)

    def test_actor_permissions(self) -> None:
        actor = Actor(name="BloodBankManager", mayPerform=[Permission.READ, Permission.WRITE])
        assert actor.name == "BloodBankManager"
        assert Permission.READ in actor.mayPerform
        assert Permission.ADMIN not in actor.mayPerform
