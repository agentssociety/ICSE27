from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the User domain class

Package: repository.user
Layer: repository
Related tasks: #157, #158, #159, #160, #161, #162, #163, #164, #165, #166, #168, #169, #170, #171, #172, #173, #174, #175, #176, #177, #178, #180, #181
Requirement coverage:
- User Registration
- Create a User Profile
- User can create a text post and optionally upload images
- User can like and unlike a post
- Add, edit, and delete comments on posts
"""

class RegistrationPage(Protocol):
    def submitRegistration(self) -> None:
        ...

    def submitRegistration(self, email: Any, password: Any) -> None:
        ...

    def returnError(self, Invalid_email_format: Any) -> None:
        ...

    def returnError(self, Email_already_in_use: Any) -> None:
        ...

    def redirectToLogin(self, Account_created_Warning: "Confirmationemailmaybedelayed.") -> None:
        ...

    def redirectToLogin(self, Account_created_Please_check_email_to_confirm: Any) -> None:
        ...

class UserDatabase(Protocol):
    def findByEmail(self) -> None:
        ...

    def insertUser(self) -> None:
        ...

class EmailNotificationSystem(Protocol):
    def sendConfirmationEmail(self) -> None:
        ...

class EmailValidator(Protocol):
    def validateFormat(self) -> None:
        ...

class AccountManagementService(Protocol):
    ...

class UserDataRepository(Protocol):
    ...