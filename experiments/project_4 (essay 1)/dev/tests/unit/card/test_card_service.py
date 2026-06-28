from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from src.service.card.card_service import AuthenticationFlow


class TestCardAuthenticationFlow:
    def test_authenticate_with_data(self) -> None:
        mock_repo = MagicMock()
        flow = AuthenticationFlow(mock_repo)
        result = flow.authenticate("card_data", "pin_data")
        assert result is True
