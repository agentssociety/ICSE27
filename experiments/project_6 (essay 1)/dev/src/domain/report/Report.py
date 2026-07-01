from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.domain.post import Post
    from src.domain.user import User

"""
Domain layer for the Report domain class

Package: domain.report
Layer: domain
Related tasks: #172, #173
Requirement coverage:
- User should be able to report a post by selecting a reason from a dropdown menu
- Admin Reported Content Panel
"""

@dataclass
class Report:
    user: User
    post: Post

@dataclass
class ReportId:
    pass

@dataclass
class ReportCreatedEvent:
    pass

@dataclass
class ReportUpdatedEvent:
    pass
