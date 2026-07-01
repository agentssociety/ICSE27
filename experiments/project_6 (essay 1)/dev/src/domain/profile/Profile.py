from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class Visibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class AuthenticationStatus(Enum):
    AUTHENTICATED = "authenticated"
    UNAUTHENTICATED = "unauthenticated"

@dataclass
class Photo:
    url: str
    caption: str = ""

@dataclass
class Biography:
    text: str

    def validate(self) -> bool:
        return len(self.text) <= 500

@dataclass
class AuditEntry:
    action: str
    timestamp: str
    userId: str

@dataclass
class Profile:
    id: str
    userId: str
    displayName: str
    photo: Photo | None = None
    biography: Biography | None = None
    visibility: Visibility = Visibility.PUBLIC
    followersCount: int = 0
    followingCount: int = 0

    def updateBio(self, text: str) -> bool:
        bio = Biography(text=text)
        if bio.validate():
            self.biography = bio
            return True
        return False

@dataclass
class ProfileId:
    value: str

@dataclass
class ProfileCreatedEvent:
    profileId: str

@dataclass
class ProfileUpdatedEvent:
    profileId: str
