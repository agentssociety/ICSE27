from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.domain.reward_store import RedemptionItem
    from src.domain.student import Student
    from src.domain.study_tip import Actor, Permission, Resource, State
    from src.repository.study_tip import Interface

@dataclass
class RewardItemService:
    def get_all_items(self) -> list[Any]:
        return []

    def get_item_by_id(self, item_id: str) -> Any:
        return None

    def create_item(self, name: str, cost: float, description: str = "") -> Any:
        return {"name": name, "cost": cost, "description": description}
