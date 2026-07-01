from __future__ import annotations

import pytest
from src.service.student_profile.student_profile_service import RegistrationService, RegistrationInput


class TestRegistrationInput:
    def test_init_with_values(self) -> None:
        inp = RegistrationInput(name="Bob", email="bob@test.com", password="pass123")
        assert inp.getName() == "Bob"
        assert inp.getEmail() == "bob@test.com"
        assert inp.getPassword() == "pass123"

    def test_init_defaults(self) -> None:
        inp = RegistrationInput()
        assert inp.getName() == ""
        assert inp.getEmail() == ""
        assert inp.getPassword() == ""
