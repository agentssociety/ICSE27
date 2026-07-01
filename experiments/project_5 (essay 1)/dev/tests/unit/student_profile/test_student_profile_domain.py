from __future__ import annotations

import pytest
from src.domain.student_profile import StudentProfile
from src.domain.nugget_wallet import NuggetWallet
from src.domain.badge import Badge


class TestStudentProfileDomain:
    def test_create_student_profile(self) -> None:
        profile = StudentProfile(student_id="student1")
        assert profile.student_id == "student1"
        assert profile.avatar_url == ""
        assert profile.bio == ""

    def test_nugget_wallet_initially_zero(self) -> None:
        wallet = NuggetWallet(student_id="student1")
        assert wallet.get_balance() == 0.0

    def test_add_nuggets(self) -> None:
        wallet = NuggetWallet(student_id="student1")
        wallet.add_nuggets(50.0)
        assert wallet.get_balance() == 50.0

    def test_deduct_nuggets_insufficient(self) -> None:
        wallet = NuggetWallet(student_id="student1")
        result = wallet.deduct_nuggets(100.0)
        assert result is False
        assert wallet.get_balance() == 0.0

    def test_badge_display(self) -> None:
        badge = Badge(name="Gold Star", description="Awarded for excellence")
        assert badge.display() == "Gold Star: Awarded for excellence"
