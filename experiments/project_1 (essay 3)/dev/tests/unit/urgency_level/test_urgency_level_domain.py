from __future__ import annotations

import pytest
from src.domain.urgency_level.UrgencyLevel import (
    UrgencyLevel, UrgencyLevelValue, Resource, Actor, Permission, State, Interface
)


class TestUrgencyLevel:
    def test_create_valid_level(self):
        u = UrgencyLevel(level=3)
        assert u.level == 3
        assert u.label == "Medium"

    def test_create_invalid_level_low(self):
        with pytest.raises(ValueError):
            UrgencyLevel(level=0)

    def test_create_invalid_level_high(self):
        with pytest.raises(ValueError):
            UrgencyLevel(level=6)

    def test_increase(self):
        u = UrgencyLevel(level=2)
        u2 = u.increase()
        assert u2.level == 3

    def test_increase_max(self):
        u = UrgencyLevel(level=5)
        with pytest.raises(ValueError):
            u.increase()

    def test_decrease(self):
        u = UrgencyLevel(level=4)
        u2 = u.decrease()
        assert u2.level == 3

    def test_decrease_min(self):
        u = UrgencyLevel(level=1)
        with pytest.raises(ValueError):
            u.decrease()

    def test_labels(self):
        assert UrgencyLevel(1).label == "Lowest"
        assert UrgencyLevel(5).label == "Highest"

    def test_urgency_level_value_enum(self):
        assert UrgencyLevelValue.LOWEST.value == 1
        assert UrgencyLevelValue.HIGHEST.value == 5

    def test_resource_set_urgency(self):
        actor = Actor(mayPerform=frozenset({Permission.READ}))
        resource = Resource(owner=actor, accessible={actor})
        urgency = UrgencyLevel(level=3)
        resource.setUrgency(urgency)
        assert resource.urgency == urgency

    def test_actor_has_permission(self):
        actor = Actor(mayPerform=frozenset({Permission.READ, Permission.WRITE}))
        assert actor.hasPermission(Permission.READ)
        assert actor.hasPermission(Permission.WRITE)
        assert not actor.hasPermission(Permission.ADMIN)

    def test_state_transitions(self):
        state = State()
        assert state.transitionTo("Post1") is True
    