from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the DailyWithdrawalLimit domain class

Package: repository.daily_withdrawal_limit
Layer: repository
Related tasks: #97, #98
Requirement coverage:
- Decline Withdrawals Exceeding Account Balance or Daily Limit
- Atomic Withdrawal Transactions
"""

class DailyWithdrawalLimitRepository(Protocol):
    ...
