from __future__ import annotations

import pytest
from datetime import date, timedelta

from src.domain.blood_unit.BloodUnit import (
    ABO,
    Rh,
    BloodUnit,
    BloodUnitId,
    BloodUnitCreatedEvent,
    BloodUnitUpdatedEvent,
    BLOOD_UNIT_SHELF_DAYS,
)

"""Unit tests for BloodUnit domain

Related tasks: #25, #27, #28, #29, #30, #31
"""


class TestABO:
    def test_abo_values(self) -> None:
        assert ABO.A.value == "a"
        assert ABO.B.value == "b"
        assert ABO.AB.value == "ab"
        assert ABO.O.value == "o"


class TestRh:
    def test_rh_values(self) -> None:
        assert Rh.POSITIVE.value == "positive"
        assert Rh.NEGATIVE.value == "negative"


class TestBloodUnit:
    def test_creation_with_default_expiration(self) -> None:
        donation_date = date(2024, 1, 1)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=donation_date)
        assert unit.bloodType == ABO.A
        assert unit.rhFactor == Rh.POSITIVE
        assert unit.donationDate == donation_date
        expected_expiration = donation_date + timedelta(days=BLOOD_UNIT_SHELF_DAYS)
        assert unit.expirationDate == expected_expiration

    def test_creation_with_custom_expiration(self) -> None:
        donation_date = date(2024, 1, 1)
        custom_expiration = date(2024, 2, 15)
        unit = BloodUnit(
            bloodType=ABO.O,
            rhFactor=Rh.NEGATIVE,
            donationDate=donation_date,
            expirationDate=custom_expiration,
        )
        assert unit.expirationDate == custom_expiration

    def test_get_blood_type(self) -> None:
        unit = BloodUnit(bloodType=ABO.B, rhFactor=Rh.POSITIVE, donationDate=date.today())
        assert unit.getBloodType() == ABO.B

    def test_get_rh_factor(self) -> None:
        unit = BloodUnit(bloodType=ABO.AB, rhFactor=Rh.NEGATIVE, donationDate=date.today())
        assert unit.getRhFactor() == Rh.NEGATIVE

    def test_get_donation_date(self) -> None:
        donation_date = date(2024, 3, 15)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=donation_date)
        assert unit.getDonationDate() == donation_date

    def test_set_expiration_date(self) -> None:
        unit = BloodUnit(bloodType=ABO.O, rhFactor=Rh.POSITIVE, donationDate=date.today())
        new_expiration = date.today() + timedelta(days=30)
        unit.setExpirationDate(new_expiration)
        assert unit.expirationDate == new_expiration

    def test_is_not_expired(self) -> None:
        future_date = date.today() + timedelta(days=10)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=future_date)
        assert not unit.isExpired()

    def test_is_expired(self) -> None:
        past_date = date.today() - timedelta(days=1)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=past_date)
        assert unit.isExpired()

    def test_days_until_expiration_positive(self) -> None:
        future_date = date.today() + timedelta(days=10)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=future_date)
        assert unit.daysUntilExpiration() == 10

    def test_days_until_expiration_negative(self) -> None:
        past_date = date.today() - timedelta(days=5)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=past_date)
        assert unit.daysUntilExpiration() == -5

    def test_compatibility_o_negative_universal(self) -> None:
        """O- is universal donor, compatible with all recipients."""
        unit = BloodUnit(bloodType=ABO.O, rhFactor=Rh.NEGATIVE, donationDate=date.today())
        assert unit.isCompatibleWith(ABO.A, Rh.POSITIVE)
        assert unit.isCompatibleWith(ABO.B, Rh.NEGATIVE)
        assert unit.isCompatibleWith(ABO.AB, Rh.POSITIVE)
        assert unit.isCompatibleWith(ABO.O, Rh.NEGATIVE)

    def test_compatibility_a_positive(self) -> None:
        """A+ can donate to A+ and AB+."""
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today())
        assert unit.isCompatibleWith(ABO.A, Rh.POSITIVE)
        assert unit.isCompatibleWith(ABO.AB, Rh.POSITIVE)
        assert not unit.isCompatibleWith(ABO.B, Rh.POSITIVE)
        assert not unit.isCompatibleWith(ABO.O, Rh.POSITIVE)

    def test_compatibility_rh_positive_to_negative(self) -> None:
        """Rh+ cannot donate to Rh-."""
        unit = BloodUnit(bloodType=ABO.O, rhFactor=Rh.POSITIVE, donationDate=date.today())
        assert not unit.isCompatibleWith(ABO.A, Rh.NEGATIVE)

    def test_compatibility_rh_negative_to_positive(self) -> None:
        """Rh- can donate to Rh+."""
        unit = BloodUnit(bloodType=ABO.O, rhFactor=Rh.NEGATIVE, donationDate=date.today())
        assert unit.isCompatibleWith(ABO.A, Rh.POSITIVE)

    def test_compatibility_ab_positive(self) -> None:
        """AB+ can only donate to AB+."""
        unit = BloodUnit(bloodType=ABO.AB, rhFactor=Rh.POSITIVE, donationDate=date.today())
        assert unit.isCompatibleWith(ABO.AB, Rh.POSITIVE)
        assert not unit.isCompatibleWith(ABO.A, Rh.POSITIVE)
        assert not unit.isCompatibleWith(ABO.B, Rh.POSITIVE)

    def test_b_compatible_with_b_and_ab(self) -> None:
        """B can donate to B and AB."""
        unit = BloodUnit(bloodType=ABO.B, rhFactor=Rh.NEGATIVE, donationDate=date.today())
        assert unit.isCompatibleWith(ABO.B, Rh.POSITIVE)
        assert unit.isCompatibleWith(ABO.AB, Rh.POSITIVE)
        assert not unit.isCompatibleWith(ABO.A, Rh.POSITIVE)

    def test_is_expiring_when_close_to_expiry(self) -> None:
        """Blood unit within 7 days of expiry should be flagged as expiring."""
        near_expiry = date.today() + timedelta(days=3)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=near_expiry)
        assert unit.isExpiring is True

    def test_is_not_expiring_when_far_from_expiry(self) -> None:
        """Blood unit more than 7 days from expiry should not be flagged."""
        far_expiry = date.today() + timedelta(days=20)
        unit = BloodUnit(bloodType=ABO.A, rhFactor=Rh.POSITIVE, donationDate=date.today(), expirationDate=far_expiry)
        assert unit.isExpiring is False


class TestBloodUnitId:
    def test_creation(self) -> None:
        unit_id = BloodUnitId(id="unit-001")
        assert unit_id.id == "unit-001"


class TestBloodUnitEvents:
    def test_created_event(self) -> None:
        unit_id = BloodUnitId(id="unit-001")
        event = BloodUnitCreatedEvent(blood_unit_id=unit_id)
        assert event.blood_unit_id.id == "unit-001"
        assert event.timestamp is not None

    def test_updated_event(self) -> None:
        unit_id = BloodUnitId(id="unit-001")
        event = BloodUnitUpdatedEvent(blood_unit_id=unit_id)
        assert event.blood_unit_id.id == "unit-001"
        assert event.timestamp is not None
