from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class State(Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class Permission(Enum):
    SEND = "send"
    READ_OWN = "read_own"

@dataclass
class Actor:
    userId: str

@dataclass
class Resource:
    type: str
    id: str

@dataclass
class Message:
    id: str
    senderId: str
    receiverId: str
    content: str
    state: State = State.SENT
    createdAt: str = ""

@dataclass
class MessageId:
    value: str

@dataclass
class MessageCreatedEvent:
    messageId: str

@dataclass
class MessageUpdatedEvent:
    messageId: str
