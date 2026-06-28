from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAccountAPI:
    def test_list_accounts(self) -> None:
        pytest.skip("Requires database connection")

    def test_get_account_not_found(self) -> None:
        pytest.skip("Requires database connection")
