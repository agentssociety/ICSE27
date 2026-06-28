from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the Account domain class

Package: repository.account
Layer: repository
Related tasks: #96, #97, #98, #99, #100
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
- Decline Withdrawals Exceeding Account Balance or Daily Limit
- Atomic Withdrawal Transactions
- Detection and Flagging of Suspicious Withdrawal Patterns
- Admin User Management and Transaction Review
"""

class AccountRepository(Protocol):
    ...
