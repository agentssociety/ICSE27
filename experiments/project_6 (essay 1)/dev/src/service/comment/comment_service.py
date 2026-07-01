from __future__ import annotations

from typing import Any, Protocol

"""
Service layer for the Comment domain class

Package: service.comment
Layer: service
Related tasks: #161, #169
Requirement coverage:
- Add, edit, and delete comments on posts
- User receives notification on post interactions
"""

class CommentService(Protocol):
    ...
