from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from src.domain.reward_store import RedemptionItem
    from src.domain.student import Student
    from src.domain.study_tip import Actor, Permission, Resource, State
    from src.repository.study_tip import Interface

@dataclass
class RewardStoreService:
    def get_store(self, store_id: str) -> Any:
        return None

    def list_available_items(self) -> list[Any]:
        return []

    def add_item_to_store(self, store_id: str, item: Any) -> None:
        pass
