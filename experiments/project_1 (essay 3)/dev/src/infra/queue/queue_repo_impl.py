from __future__ import annotations

from typing import Any

"""
Infra layer for the Queue domain class

Package: infra.queue
Layer: infra
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

class SQLAlchemyQueueRepository:
    def __init__(self) -> None:
        pass
