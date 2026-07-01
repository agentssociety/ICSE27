from __future__ import annotations

import pytest
from src.api.nugget_wallet.nugget_wallet_router import RegistrationController, RegistrationInput


class TestRegistrationController:
    def test_handle_registration(self) -> None:
        controller = RegistrationController()
        result = controller.handleRegistration(RegistrationInput(name="Charlie", email="c@d.com", password="pass"))
        assert "Charlie" in result

    def test_init(self) -> None:
        controller = RegistrationController()
        assert controller is not None
