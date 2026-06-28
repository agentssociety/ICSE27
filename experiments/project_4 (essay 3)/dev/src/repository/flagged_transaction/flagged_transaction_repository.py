from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the FlaggedTransaction domain class

Package: repository.flagged_transaction
Layer: repository
Related tasks: #99, #100
Requirement coverage:
- Detection and Flagging of Suspicious Withdrawal Patterns
- Admin User Management and Transaction Review
"""

class FlaggedTransactionRepository(Protocol):
    ...
