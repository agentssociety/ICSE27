from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    pass

class RegistrationService(Protocol):
    def register(self, input: RegistrationInput) -> str:
        ...

    def validateInput(self, input: RegistrationInput) -> bool:
        ...

class RegistrationInput:
    def __init__(self, name: str | None = None, email: str | None = None, password: str | None = None) -> None:
        self.name = name
        self.email = email
        self.password = password

    def getName(self) -> str:
        return self.name or ""

    def getEmail(self) -> str:
        return self.email or ""

    def getPassword(self) -> str:
        return self.password or ""
