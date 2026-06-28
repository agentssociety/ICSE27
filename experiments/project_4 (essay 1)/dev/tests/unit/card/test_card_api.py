from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestCardAPI:
    def test_list_cards(self) -> None:
        pytest.skip("Requires database connection")

    def test_get_card_not_found(self) -> None:
        pytest.skip("Requires database connection")
