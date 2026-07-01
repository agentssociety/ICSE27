from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.bookmark import Bookmark, LoginStatus, SavedList
    from src.domain.comment import Comment
    from src.domain.friendship import Friendship, OnlineStatus
    from src.domain.group_membership import GroupMembership
    from src.domain.like import Like
    from src.domain.message import Message
    from src.domain.notification_preference import NotificationPreference
    from src.domain.post import Post
    from src.domain.profile import AuthenticationStatus, Profile, Role
    from src.domain.report import Report


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    INVARIANTS = "invariants"
    FIELD_ADMIN_SUBSUMES_ALL = "field_admin_subsumes_all"
    FIELD_WRITE_SUBSUMES_READ = "field_write_subsumes_read"
    FIELD_EXECUTE_SUBSUMES_READ = "field_execute_subsumes_read"


class State(Enum):
    PREIDLE = "preidle"
    POST1_ACCOUNTCREATED = "post1_accountcreated"
    POST2_EMAILSENT = "post2_emailsent"
    POST3_REDIRECTED = "post3_redirected"


class InterfaceKind(Enum):
    DATABASE = "database"
    EMAIL_SERVICE = "email_service"
    EMAILVALIDKIND = "emailvalidkind"
    API = "api"


class AccountStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"


class UserAccountStatus(Enum):
    ACTIVE = "active"
    GRACEPERIOD = "graceperiod"
    DELETED = "deleted"
    RECOVERED = "recovered"


@dataclass
class Resource:
    pass


@dataclass(frozen=True)
class Actor:
    mayPerform: set[Permission]

    def checkPermission(self, initiator: Actor, permission: Permission) -> bool:
        return permission in self.mayPerform

    def __hash__(self) -> int:
        return hash(id(self))


@dataclass
class Interface:
    kind: InterfaceKind
    encrypted: bool
    authenticated: bool


@dataclass
class UserAccount:
    email: str
    password: str
    status: AccountStatus
    owner: Actor
    accessible: set[Actor]

    def create(self, email: str, hashedPassword: str, accountStatus: AccountStatus = AccountStatus.PENDING) -> None:
        self.email = email
        self.password = hashedPassword
        self.status = accountStatus

    def checkStatus(self) -> AccountStatus:
        return self.status

    def checkAccessible(self, initiator: Actor) -> bool:
        return initiator in self.accessible

    def setStatus(self, newStatus: AccountStatus) -> None:
        self.status = newStatus


@dataclass
class EmailConfirmation:
    sent: bool

    def create(self, userAccount: UserAccount, triggeredBy_REQ_REG_01: Any) -> None:
        self.sent = True


@dataclass
class REQ_REG_01:
    pass

    def result(self, null_or_account: Any) -> None:
        pass


@dataclass
class Operation:
    initiator: Actor
    target: set[UserAccount]
    channel: set[Interface]
    grant: Permission
    pre: State
    post: State

    def createOperation(self, initiator: Actor, targets: set[UserAccount], channels: set[Interface], permission: Permission, preState: State, postState: State) -> None:
        self.initiator = initiator
        self.target = targets
        self.channel = channels
        self.grant = permission
        self.pre = preState
        self.post = postState


@dataclass
class User:
    loggedIn: bool
    role: Role | None
    userId: str
    isAuthenticated: bool
    id: str
    authentication_status: AuthenticationStatus | None
    identity: str
    onlineStatus: OnlineStatus | None
    abstract_mustBeLoggedIn: bool
    abstract_cannotSendRequestToSelf_recipient: User | None
    mayPerform: set[Permission]
    username: str
    field_isLoggedIn: bool
    loginStatus: LoginStatus | None
    rolePermissions: list[Permission]
    passwordHash: str
    email: str
    accountStatus: str
    permissions: list[Permission]
    name: str
    notificationEnabled: bool
    profile: Profile | None = None
    savedList: SavedList | None = None
    posts: list[Post] = field(default_factory=list)
    notificationPreferences: list[NotificationPreference] = field(default_factory=list)
    friendships: list[Friendship] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)
    likes: list[Like] = field(default_factory=list)
    bookmarks: list[Bookmark] = field(default_factory=list)
    reports: list[Report] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    groupMemberships: list[GroupMembership] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.mayPerform = set(self.permissions) if hasattr(self, 'permissions') and self.permissions else set()

    def hasPermission(self, permission: Permission) -> bool:
        return permission in self.mayPerform

    def getAuthenticationStatus(self) -> AuthenticationStatus | None:
        return self.authentication_status

    def getRole(self) -> Role | None:
        return self.role

    def applyAction(self, actionType: str) -> None:
        pass

    def applyWarning(self) -> None:
        pass

    def checkPermission(self, permission: Permission) -> bool:
        return self.hasPermission(permission)

    def validateNotSelf(self, targetUser: User) -> None:
        if self.userId == targetUser.userId:
            raise ValueError("Cannot perform action on self")

    def checkLoginStatus(self, token: str) -> LoginStatus | None:
        return self.loginStatus

    def getSavedList(self) -> SavedList | None:
        return self.savedList

    def checkAuthentication(self, sessionToken: str) -> None:
        if not self.isAuthenticated:
            raise PermissionError("User is not authenticated")

    def notifyViewHistory(self) -> None:
        pass

    def validateEmailFormat(self, newEmail: str) -> bool:
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, newEmail))

    def cascadeDelete(self) -> None:
        self.posts.clear()
        self.notificationPreferences.clear()
        self.friendships.clear()
        self.messages.clear()
        self.likes.clear()
        self.bookmarks.clear()
        self.reports.clear()
        self.comments.clear()
        self.groupMemberships.clear()

    def getPermission(self, user: User) -> Permission:
        if self.userId == user.userId:
            return Permission.ADMIN
        return Permission.READ

    def isOwner(self, user: User, comment: Comment) -> bool:
        return self.userId == user.userId

    def isLoggedIn(self) -> bool:
        return self.loggedIn

    def hasNotificationsEnabled(self) -> bool:
        return self.notificationEnabled


@dataclass
class UserId:
    pass


@dataclass
class UserCreatedEvent:
    userId: str
    email: str


@dataclass
class UserUpdatedEvent:
    userId: str
