from __future__ import annotations

import pytest
from src.api.student.student_router import RegistrationController, RegistrationInput


class TestRegistrationController:
    def test_handle_registration(self) -> None:
        controller = RegistrationController()
        result = controller.handleRegistration(RegistrationInput(name="Alice", email="a@b.com", password="pass"))
        assert "Alice" in result

    def test_init(self) -> None:
        controller = RegistrationController()
        assert controller is not None
