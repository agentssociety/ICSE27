from __future__ import annotations

import pytest
from src.domain.urgency_level.UrgencyLevel import UrgencyLevel, Resource, Actor, Permission
from src.service.urgency_level.urgency_level_service import UrgencyAssignmentService


class TestUrgencyAssignmentService:
    def test_assign_urgency(self):
        actor = Actor(mayPerform=frozenset({Permission.ADMIN}))
        resource = Resource(owner=actor, accessible={actor})
        urgency = UrgencyLevel(level=3)
        service = UrgencyAssignmentService()
        result = service.assign_urgency(resource, urgency)
        assert result.urgency == urgency
        assert result.urgency.level == 3
