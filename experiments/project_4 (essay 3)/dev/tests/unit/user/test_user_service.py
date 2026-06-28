from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse
from src.service.user.user_service import UserService


class TestUserService:

    def test_create_user(self) -> None:
        mock_session = MagicMock()
        service = UserService(session=mock_session)

        req = UserCreateRequest(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_pw",
            role="regular_user",
        )
        result = service.create_user(req)
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.role == "regular_user"
        assert result.status == "active"

    def test_list_users(self) -> None:
        mock_session = MagicMock()
        service = UserService(session=mock_session)

        result = service.list_users()
        assert result is not None
        assert hasattr(result, 'items')
        assert hasattr(result, 'total')

    def test_get_user_not_found(self) -> None:
        mock_session = MagicMock()
        service = UserService(session=mock_session)

        result = service.get_user("nonexistent_id")
        assert result is None

    def test_deactivate_user(self) -> None:
        mock_session = MagicMock()
        service = UserService(session=mock_session)

        result = service.deactivate_user("nonexistent")
        assert result is None

    def test_activate_user(self) -> None:
        mock_session = MagicMock()
        service = UserService(session=mock_session)

        result = service.activate_user("nonexistent")
        assert result is None
