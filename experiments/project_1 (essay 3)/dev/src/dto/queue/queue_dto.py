from __future__ import annotations

from typing import Any
from pydantic import BaseModel

"""
Dto layer for the Queue domain class

Package: dto.queue
Layer: dto
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

class QueueCreateRequest(BaseModel):
    pass

class QueueUpdateRequest(BaseModel):
    pass

class QueueResponse(BaseModel):
    pass