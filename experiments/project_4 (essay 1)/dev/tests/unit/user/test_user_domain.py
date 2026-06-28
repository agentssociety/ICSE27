from __future__ import annotations

import pytest
from src.domain.user import User, AccountState, Permission, Actor, UserId, UserCreatedEvent, UserUpdatedEvent


class TestUserDomain:
    def test_actor_creation(self) -> None:
        actor = Actor(mayPerform={Permission.READ}, id="actor1", name="Test Actor")
        assert actor.id == "actor1"
        assert actor.name == "Test Actor"
        assert Permission.READ in actor.mayPerform

    def test_permission_check(self) -> None:
        actor = Actor(mayPerform={Permission.READ, Permission.WRITE}, id="actor1", name="Admin")
        assert actor.hasPermission(actor, None, Permission.READ)
        assert not actor.hasPermission(actor, None, Permission.ADMIN)
