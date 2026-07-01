from __future__ import annotations

import pytest
from src.api.badge.badge_router import RegistrationController, RegistrationInput


class TestRegistrationController:
    def test_handle_registration(self) -> None:
        controller = RegistrationController()
        result = controller.handleRegistration(RegistrationInput(name="Diana", email="d@e.com", password="pass"))
        assert "Diana" in result

    def test_init(self) -> None:
        controller = RegistrationController()
        assert controller is not None
