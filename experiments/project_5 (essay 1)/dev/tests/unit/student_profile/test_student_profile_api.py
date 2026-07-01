from __future__ import annotations

import pytest
from src.api.student_profile.student_profile_router import RegistrationController, RegistrationInput


class TestRegistrationController:
    def test_handle_registration(self) -> None:
        controller = RegistrationController()
        result = controller.handleRegistration(RegistrationInput(name="Bob", email="b@c.com", password="pass"))
        assert "Bob" in result

    def test_init(self) -> None:
        controller = RegistrationController()
        assert controller is not None
