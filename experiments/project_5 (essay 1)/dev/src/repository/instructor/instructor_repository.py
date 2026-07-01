from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the Instructor domain class

Package: repository.instructor
Layer: repository
Related tasks: #105
Requirement coverage:
- Instructor Registration and Login
"""

class Registration_API(Protocol):
    ...

class Login_API(Protocol):
    ...

class User_Database(Protocol):
    ...

class Dashboard_UI(Protocol):
    ...
