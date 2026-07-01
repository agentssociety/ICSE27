from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    pass

"""
Domain layer for the NuggetWallet domain class

Package: domain.nugget_wallet
Layer: domain
Related tasks: #109, #110, #111, #112, #114, #115
Requirement coverage:
- Manual Bonus Nugget Granting with Justification
- Create Student Profile During Registration
- Single Question Per Screen Exam Interface
- Streak System Implementation
- Student should be able to redeem nuggets for rewards
"""

@dataclass
class NuggetWallet:
    student_id: str
    balance: float = 0.0

    def add_nuggets(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Cannot add negative nuggets")
        self.balance += amount

    def deduct_nuggets(self, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Cannot deduct negative nuggets")
        if self.balance < amount:
            return False
        self.balance -= amount
        return True

    def get_balance(self) -> float:
        return self.balance

@dataclass
class NuggetWalletId:
    pass

@dataclass
class NuggetWalletCreatedEvent:
    pass

@dataclass
class NuggetWalletUpdatedEvent:
    pass
