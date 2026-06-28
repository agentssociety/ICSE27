from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserAPI:
    def test_list_users(self) -> None:
        pytest.skip("Requires database connection")

    def test_get_user_not_found(self) -> None:
        pytest.skip("Requires database connection")
