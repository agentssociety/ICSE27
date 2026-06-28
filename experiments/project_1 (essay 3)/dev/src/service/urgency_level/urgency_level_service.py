from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.urgency_level import Actor, Permission, State, UrgencyLevel

"""
Service layer for the UrgencyLevel domain class

Package: service.urgency_level
Layer: service
Related tasks: #54, #55, #56, #58
Requirement coverage:
- Assign Item Urgency Level
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Real-time live dashboard displaying urgency and wait time
"""

from src.domain.urgency_level.UrgencyLevel import UrgencyLevel, Resource, Actor, Permission


class UrgencyAssignmentService:
    def assign_urgency(self, resource: Resource, new_urgency: UrgencyLevel) -> Resource:
        resource.setUrgency(new_urgency)
        resource.saveState()
        return resource
