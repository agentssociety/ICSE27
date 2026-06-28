from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api.user.user_router import router


class TestUserAPI:

    def test_router_exists(self) -> None:
        assert router is not None
        assert len(router.routes) > 0

    def test_list_endpoint_exists(self) -> None:
        from src.api.user.user_router import list_users
        assert list_users is not None

    def test_create_endpoint_exists(self) -> None:
        from src.api.user.user_router import create_user
        assert create_user is not None

    def test_get_endpoint_exists(self) -> None:
        from src.api.user.user_router import get_user
        assert get_user is not None

    def test_update_endpoint_exists(self) -> None:
        from src.api.user.user_router import update_user
        assert update_user is not None

    def test_deactivate_endpoint_exists(self) -> None:
        from src.api.user.user_router import deactivate_user
        assert deactivate_user is not None

    def test_activate_endpoint_exists(self) -> None:
        from src.api.user.user_router import activate_user
        assert activate_user is not None

    def test_delete_endpoint_exists(self) -> None:
        from src.api.user.user_router import delete_user
        assert delete_user is not None

    def test_create_user_validation(self) -> None:
        from src.dto.user.user_dto import UserCreateRequest
        with pytest.raises(ValueError, match="Username is required"):
            UserCreateRequest(
                username="",
                email="test@test.com",
                password_hash="hash",
            )

    def test_user_response_model(self) -> None:
        from src.dto.user.user_dto import UserResponse
        from datetime import datetime
        resp = UserResponse(
            id="usr-001",
            username="testuser",
            email="test@example.com",
            role="regular_user",
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        assert resp.id == "usr-001"
        assert resp.role == "regular_user"
