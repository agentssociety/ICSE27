from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the Queue domain class

Package: repository.queue
Layer: repository
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

class QueueRepository(Protocol):
    ...
