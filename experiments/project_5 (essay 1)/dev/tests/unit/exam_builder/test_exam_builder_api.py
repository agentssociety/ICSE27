from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from main import app


class TestExamBuilderApi:
    client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")
        assert response.status_code == 200
