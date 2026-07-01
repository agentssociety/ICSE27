from __future__ import annotations

import pytest
from src.service.badge.badge_service import RegistrationService, RegistrationInput


class TestRegistrationInput:
    def test_init_with_values(self) -> None:
        inp = RegistrationInput(name="Alice", email="alice@test.com", password="secret")
        assert inp.getName() == "Alice"
        assert inp.getEmail() == "alice@test.com"
        assert inp.getPassword() == "secret"

    def test_init_defaults(self) -> None:
        inp = RegistrationInput()
        assert inp.getName() == ""
        assert inp.getEmail() == ""
        assert inp.getPassword() == ""

    def test_getters_return_empty_for_none(self) -> None:
        inp = RegistrationInput(name=None, email=None, password=None)
        assert inp.getName() == ""
        assert inp.getEmail() == ""
        assert inp.getPassword() == ""
