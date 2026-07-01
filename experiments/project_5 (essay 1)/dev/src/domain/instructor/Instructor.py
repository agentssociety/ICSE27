from __future__ import annotations
from typing import Any
from dataclasses import dataclass

@dataclass
class Instructor:
    name: str
    email: str
    department: str = ""

@dataclass
class InstructorId:
    pass

@dataclass
class InstructorCreatedEvent:
    pass

@dataclass
class InstructorUpdatedEvent:
    pass
