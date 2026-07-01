from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    pass

@dataclass
class NuggetWalletService:
    def add_nuggets(self, wallet_id: str, amount: float) -> float:
        if amount < 0:
            raise ValueError("Cannot add negative nuggets")
        return amount

    def deduct_nuggets(self, wallet_id: str, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Cannot deduct negative nuggets")
        return True

    def get_balance(self, wallet_id: str) -> float:
        return 0.0
