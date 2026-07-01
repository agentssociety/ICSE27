# Project 16 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 139 |
| Requirements linked | 25 |
| Tasks | 25 |
| Domain classes | 17 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.user` · layer: `domain`

Path: `src/domain/user`
> Domain layer for the User domain class

| File | Classes |
|------|---------|
| `User.py` | `UserAccount`, `AccountStatus`, `EmailConfirmation`, `Resource`, `Actor`, `Permission`, `State`, `Interface`, `InterfaceKind`, `REQ_REG_01`, `UserAccountStatus`, `Operation`, `User`, `UserId`, `UserCreatedEvent`, `UserUpdatedEvent` |

### `dto.user` · layer: `dto`

Path: `src/dto/user`
> Dto layer for the User domain class

| File | Classes |
|------|---------|
| `user_dto.py` | `SoftDeleteRequest`, `RecoveryRequest`, `AccountStatusResponse` |

### `repository.user` · layer: `repository`

Path: `src/repository/user`
> Repository layer for the User domain class

| File | Classes |
|------|---------|
| `user_repository.py` | `RegistrationPage`, `UserDatabase`, `EmailNotificationSystem`, `EmailValidator`, `AccountManagementService`, `UserDataRepository` |

### `orm.user` · layer: `orm`

Path: `src/orm/user`
> Orm layer for the User domain class

| File | Classes |
|------|---------|
| `user_orm.py` | `UserORM` |

### `infra.user` · layer: `infra`

Path: `src/infra/user`
> Infra layer for the User domain class

| File | Classes |
|------|---------|
| `user_repo_impl.py` | `SQLAlchemyUserRepository` |

### `service.user` · layer: `service`

Path: `src/service/user`
> Service layer for the User domain class

| File | Classes |
|------|---------|
| `user_service.py` | `UserService`, `UserServiceImpl` |

### `api.user` · layer: `api`

Path: `src/api/user`
> Api layer for the User domain class

| File | Classes |
|------|---------|
| `user_router.py` | `UserRouter` |

### `tests.unit.user` · layer: `tests`

Path: `tests/unit/user`
> Unit tests for User across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_user_domain.py` | — |
| `test_user_service.py` | — |
| `test_user_api.py` | — |

### `domain.audit_log` · layer: `domain`

Path: `src/domain/audit_log`
> Domain layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `AuditLog.py` | `Admin`, `AuditLog`, `Resource`, `Operation`, `Permission`, `State`, `AuditLogId`, `AuditLogCreatedEvent`, `AuditLogUpdatedEvent` |

### `dto.audit_log` · layer: `dto`

Path: `src/dto/audit_log`
> Dto layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_dto.py` | `AuditLogCreateRequest`, `AuditLogUpdateRequest`, `AuditLogResponse` |

### `repository.audit_log` · layer: `repository`

Path: `src/repository/audit_log`
> Repository layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_repository.py` | `AuditLogRepository` |

### `orm.audit_log` · layer: `orm`

Path: `src/orm/audit_log`
> Orm layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_orm.py` | `AuditLogORM` |

### `infra.audit_log` · layer: `infra`

Path: `src/infra/audit_log`
> Infra layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_repo_impl.py` | `SQLAlchemyAuditLogRepository` |

### `service.audit_log` · layer: `service`

Path: `src/service/audit_log`
> Service layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_service.py` | `AuditLogService`, `AuditLogServiceImpl` |

### `api.audit_log` · layer: `api`

Path: `src/api/audit_log`
> Api layer for the AuditLog domain class

| File | Classes |
|------|---------|
| `audit_log_router.py` | `AuditLogRouter` |

### `tests.unit.audit_log` · layer: `tests`

Path: `tests/unit/audit_log`
> Unit tests for AuditLog across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_audit_log_domain.py` | — |
| `test_audit_log_service.py` | — |
| `test_audit_log_api.py` | — |

### `domain.block` · layer: `domain`

Path: `src/domain/block`
> Domain layer for the Block domain class

| File | Classes |
|------|---------|
| `Block.py` | `BlockRecord`, `Permission`, `State`, `Block`, `BlockId`, `BlockCreatedEvent`, `BlockUpdatedEvent` |

### `dto.block` · layer: `dto`

Path: `src/dto/block`
> Dto layer for the Block domain class

| File | Classes |
|------|---------|
| `block_dto.py` | `BlockCreateRequest`, `BlockUpdateRequest`, `BlockResponse` |

### `repository.block` · layer: `repository`

Path: `src/repository/block`
> Repository layer for the Block domain class

| File | Classes |
|------|---------|
| `block_repository.py` | `UserProfileAPI`, `PostsDatabase`, `MessagesDatabase`, `NotificationSystem` |

### `orm.block` · layer: `orm`

Path: `src/orm/block`
> Orm layer for the Block domain class

| File | Classes |
|------|---------|
| `block_orm.py` | `BlockORM` |

### `infra.block` · layer: `infra`

Path: `src/infra/block`
> Infra layer for the Block domain class

| File | Classes |
|------|---------|
| `block_repo_impl.py` | `SQLAlchemyBlockRepository` |

### `service.block` · layer: `service`

Path: `src/service/block`
> Service layer for the Block domain class

| File | Classes |
|------|---------|
| `block_service.py` | `BlockService`, `BlockServiceImpl` |

### `api.block` · layer: `api`

Path: `src/api/block`
> Api layer for the Block domain class

| File | Classes |
|------|---------|
| `block_router.py` | `BlockRouter` |

### `tests.unit.block` · layer: `tests`

Path: `tests/unit/block`
> Unit tests for Block across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_block_domain.py` | — |
| `test_block_service.py` | — |
| `test_block_api.py` | — |

### `domain.follow` · layer: `domain`

Path: `src/domain/follow`
> Domain layer for the Follow domain class

| File | Classes |
|------|---------|
| `Follow.py` | `Actor`, `UserProfile`, `Permission`, `State`, `Follow`, `FollowId`, `FollowCreatedEvent`, `FollowUpdatedEvent` |

### `dto.follow` · layer: `dto`

Path: `src/dto/follow`
> Dto layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_dto.py` | `FollowRequest`, `UnfollowRequest`, `FollowResponse` |

### `repository.follow` · layer: `repository`

Path: `src/repository/follow`
> Repository layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_repository.py` | `FollowUnfollowAPI`, `UserProfileDatabase` |

### `orm.follow` · layer: `orm`

Path: `src/orm/follow`
> Orm layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_orm.py` | `FollowORM` |

### `infra.follow` · layer: `infra`

Path: `src/infra/follow`
> Infra layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_repo_impl.py` | `SQLAlchemyFollowRepository` |

### `service.follow` · layer: `service`

Path: `src/service/follow`
> Service layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_service.py` | `FollowUnfollowService` |

### `api.follow` · layer: `api`

Path: `src/api/follow`
> Api layer for the Follow domain class

| File | Classes |
|------|---------|
| `follow_router.py` | `FollowUnfollowController` |

### `tests.unit.follow` · layer: `tests`

Path: `tests/unit/follow`
> Unit tests for Follow across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_follow_domain.py` | — |
| `test_follow_service.py` | — |
| `test_follow_api.py` | — |

### `domain.friendship` · layer: `domain`

Path: `src/domain/friendship`
> Domain layer for the Friendship domain class

| File | Classes |
|------|---------|
| `Friendship.py` | `OnlineStatus`, `FriendRequestStatus`, `NotificationType`, `FriendRequest`, `Friendship`, `FriendshipId`, `FriendshipCreatedEvent`, `FriendshipUpdatedEvent` |

### `dto.friendship` · layer: `dto`

Path: `src/dto/friendship`
> Dto layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_dto.py` | `FriendshipCreateRequest`, `FriendshipUpdateRequest`, `FriendshipResponse` |

### `repository.friendship` · layer: `repository`

Path: `src/repository/friendship`
> Repository layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_repository.py` | `FriendshipRepository` |

### `orm.friendship` · layer: `orm`

Path: `src/orm/friendship`
> Orm layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_orm.py` | `FriendshipORM` |

### `infra.friendship` · layer: `infra`

Path: `src/infra/friendship`
> Infra layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_repo_impl.py` | `SQLAlchemyFriendshipRepository` |

### `service.friendship` · layer: `service`

Path: `src/service/friendship`
> Service layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_service.py` | `FriendshipService`, `FriendshipServiceImpl` |

### `api.friendship` · layer: `api`

Path: `src/api/friendship`
> Api layer for the Friendship domain class

| File | Classes |
|------|---------|
| `friendship_router.py` | `FriendshipRouter` |

### `tests.unit.friendship` · layer: `tests`

Path: `tests/unit/friendship`
> Unit tests for Friendship across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_friendship_domain.py` | — |
| `test_friendship_service.py` | — |
| `test_friendship_api.py` | — |

### `domain.group` · layer: `domain`

Path: `src/domain/group`
> Domain layer for the Group domain class

| File | Classes |
|------|---------|
| `Group.py` | `Permission`, `State`, `GroupName`, `Visibility`, `Actor`, `Resource`, `Group`, `Interface`, `IfaceKind`, `Operation`, `GroupId`, `GroupCreatedEvent`, `GroupUpdatedEvent` |

### `dto.group` · layer: `dto`

Path: `src/dto/group`
> Dto layer for the Group domain class

| File | Classes |
|------|---------|
| `group_dto.py` | `CreateGroupRequest`, `CreateGroupResponse` |

### `repository.group` · layer: `repository`

Path: `src/repository/group`
> Repository layer for the Group domain class

| File | Classes |
|------|---------|
| `group_repository.py` | `GroupCreationAPI`, `GroupDB` |

### `orm.group` · layer: `orm`

Path: `src/orm/group`
> Orm layer for the Group domain class

| File | Classes |
|------|---------|
| `group_orm.py` | `GroupORM` |

### `infra.group` · layer: `infra`

Path: `src/infra/group`
> Infra layer for the Group domain class

| File | Classes |
|------|---------|
| `group_repo_impl.py` | `SQLAlchemyGroupRepository` |

### `service.group` · layer: `service`

Path: `src/service/group`
> Service layer for the Group domain class

| File | Classes |
|------|---------|
| `group_service.py` | `GroupCreationService` |

### `api.group` · layer: `api`

Path: `src/api/group`
> Api layer for the Group domain class

| File | Classes |
|------|---------|
| `group_router.py` | `GroupController` |

### `tests.unit.group` · layer: `tests`

Path: `tests/unit/group`
> Unit tests for Group across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_group_domain.py` | — |
| `test_group_service.py` | — |
| `test_group_api.py` | — |

### `domain.group_membership` · layer: `domain`

Path: `src/domain/group_membership`
> Domain layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `GroupMembership.py` | `JoinRequestStatus`, `Permission`, `JoinRequest`, `GroupMembership`, `Role`, `GroupMembershipId`, `GroupMembershipCreatedEvent`, `GroupMembershipUpdatedEvent` |

### `dto.group_membership` · layer: `dto`

Path: `src/dto/group_membership`
> Dto layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_dto.py` | `GroupMembershipCreateRequest`, `GroupMembershipUpdateRequest`, `GroupMembershipResponse` |

### `repository.group_membership` · layer: `repository`

Path: `src/repository/group_membership`
> Repository layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_repository.py` | `JoinRequestManagementUI`, `JoinRequestsDatabase`, `GroupAPI` |

### `orm.group_membership` · layer: `orm`

Path: `src/orm/group_membership`
> Orm layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_orm.py` | `GroupMembershipORM` |

### `infra.group_membership` · layer: `infra`

Path: `src/infra/group_membership`
> Infra layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_repo_impl.py` | `SQLAlchemyGroupMembershipRepository` |

### `service.group_membership` · layer: `service`

Path: `src/service/group_membership`
> Service layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_service.py` | `GroupMembershipService`, `GroupMembershipServiceImpl` |

### `api.group_membership` · layer: `api`

Path: `src/api/group_membership`
> Api layer for the GroupMembership domain class

| File | Classes |
|------|---------|
| `group_membership_router.py` | `GroupMembershipRouter` |

### `tests.unit.group_membership` · layer: `tests`

Path: `tests/unit/group_membership`
> Unit tests for GroupMembership across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_group_membership_domain.py` | — |
| `test_group_membership_service.py` | — |
| `test_group_membership_api.py` | — |

### `domain.message` · layer: `domain`

Path: `src/domain/message`
> Domain layer for the Message domain class

| File | Classes |
|------|---------|
| `Message.py` | `Actor`, `Resource`, `Permission`, `Interface`, `IfaceKind`, `State`, `Message_Service_API`, `User_Database`, `Message`, `MessageId`, `MessageCreatedEvent`, `MessageUpdatedEvent` |

### `dto.message` · layer: `dto`

Path: `src/dto/message`
> Dto layer for the Message domain class

| File | Classes |
|------|---------|
| `message_dto.py` | `MessageCreateRequest`, `MessageUpdateRequest`, `MessageResponse` |

### `repository.message` · layer: `repository`

Path: `src/repository/message`
> Repository layer for the Message domain class

| File | Classes |
|------|---------|
| `message_repository.py` | `MessageRepository` |

### `orm.message` · layer: `orm`

Path: `src/orm/message`
> Orm layer for the Message domain class

| File | Classes |
|------|---------|
| `message_orm.py` | `MessageORM` |

### `infra.message` · layer: `infra`

Path: `src/infra/message`
> Infra layer for the Message domain class

| File | Classes |
|------|---------|
| `message_repo_impl.py` | `SQLAlchemyMessageRepository` |

### `service.message` · layer: `service`

Path: `src/service/message`
> Service layer for the Message domain class

| File | Classes |
|------|---------|
| `message_service.py` | `REQ_PRIV_MES_01`, `SendMessageOperation`, `ReceiveMessageOperation`, `ReplyToMessageOperation` |

### `api.message` · layer: `api`

Path: `src/api/message`
> Api layer for the Message domain class

| File | Classes |
|------|---------|
| `message_router.py` | `MessageRouter` |

### `tests.unit.message` · layer: `tests`

Path: `tests/unit/message`
> Unit tests for Message across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_message_domain.py` | — |
| `test_message_service.py` | — |
| `test_message_api.py` | — |

### `domain.notification_preference` · layer: `domain`

Path: `src/domain/notification_preference`
> Domain layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `NotificationPreference.py` | `NotificationPreference`, `NotificationCategory`, `Permission`, `UserState`, `NotificationPreferenceId`, `NotificationPreferenceCreatedEvent`, `NotificationPreferenceUpdatedEvent` |

### `dto.notification_preference` · layer: `dto`

Path: `src/dto/notification_preference`
> Dto layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_dto.py` | `NotificationPreferenceDTO` |

### `repository.notification_preference` · layer: `repository`

Path: `src/repository/notification_preference`
> Repository layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_repository.py` | `NotificationPreferenceRepository` |

### `orm.notification_preference` · layer: `orm`

Path: `src/orm/notification_preference`
> Orm layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_orm.py` | `NotificationPreferenceORM` |

### `infra.notification_preference` · layer: `infra`

Path: `src/infra/notification_preference`
> Infra layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_repo_impl.py` | `SQLAlchemyNotificationPreferenceRepository` |

### `service.notification_preference` · layer: `service`

Path: `src/service/notification_preference`
> Service layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_service.py` | `NotificationSettingsService` |

### `api.notification_preference` · layer: `api`

Path: `src/api/notification_preference`
> Api layer for the NotificationPreference domain class

| File | Classes |
|------|---------|
| `notification_preference_router.py` | `NotificationSettingsController` |

### `tests.unit.notification_preference` · layer: `tests`

Path: `tests/unit/notification_preference`
> Unit tests for NotificationPreference across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_notification_preference_domain.py` | — |
| `test_notification_preference_service.py` | — |
| `test_notification_preference_api.py` | — |

### `domain.post` · layer: `domain`

Path: `src/domain/post`
> Domain layer for the Post domain class

| File | Classes |
|------|---------|
| `Post.py` | `Post`, `Image`, `Permission`, `Role`, `PostState`, `PostId`, `PostCreatedEvent`, `PostUpdatedEvent` |

### `dto.post` · layer: `dto`

Path: `src/dto/post`
> Dto layer for the Post domain class

| File | Classes |
|------|---------|
| `post_dto.py` | `CreatePostRequest`, `CreatePostResponse` |

### `repository.post` · layer: `repository`

Path: `src/repository/post`
> Repository layer for the Post domain class

| File | Classes |
|------|---------|
| `post_repository.py` | `ContentDatabase`, `ImageStorageService` |

### `orm.post` · layer: `orm`

Path: `src/orm/post`
> Orm layer for the Post domain class

| File | Classes |
|------|---------|
| `post_orm.py` | `PostORM` |

### `infra.post` · layer: `infra`

Path: `src/infra/post`
> Infra layer for the Post domain class

| File | Classes |
|------|---------|
| `post_repo_impl.py` | `SQLAlchemyPostRepository` |

### `service.post` · layer: `service`

Path: `src/service/post`
> Service layer for the Post domain class

| File | Classes |
|------|---------|
| `post_service.py` | `PostService`, `PostServiceImpl` |

### `api.post` · layer: `api`

Path: `src/api/post`
> Api layer for the Post domain class

| File | Classes |
|------|---------|
| `post_router.py` | `PostCreationAPI` |

### `tests.unit.post` · layer: `tests`

Path: `tests/unit/post`
> Unit tests for Post across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_post_domain.py` | — |
| `test_post_service.py` | — |
| `test_post_api.py` | — |

### `domain.bookmark` · layer: `domain`

Path: `src/domain/bookmark`
> Domain layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `Bookmark.py` | `LoginStatus`, `Permission`, `Bookmark`, `SavedList`, `BookmarkId`, `BookmarkCreatedEvent`, `BookmarkUpdatedEvent` |

### `dto.bookmark` · layer: `dto`

Path: `src/dto/bookmark`
> Dto layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_dto.py` | `BookmarkRequest`, `BookmarkResponse`, `SavedListResponse` |

### `repository.bookmark` · layer: `repository`

Path: `src/repository/bookmark`
> Repository layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_repository.py` | `IUserDatabase` |

### `orm.bookmark` · layer: `orm`

Path: `src/orm/bookmark`
> Orm layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_orm.py` | `BookmarkORM` |

### `infra.bookmark` · layer: `infra`

Path: `src/infra/bookmark`
> Infra layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_repo_impl.py` | `SQLAlchemyBookmarkRepository` |

### `service.bookmark` · layer: `service`

Path: `src/service/bookmark`
> Service layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_service.py` | `BookmarkService` |

### `api.bookmark` · layer: `api`

Path: `src/api/bookmark`
> Api layer for the Bookmark domain class

| File | Classes |
|------|---------|
| `bookmark_router.py` | `IUserUI` |

### `tests.unit.bookmark` · layer: `tests`

Path: `tests/unit/bookmark`
> Unit tests for Bookmark across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_bookmark_domain.py` | — |
| `test_bookmark_service.py` | — |
| `test_bookmark_api.py` | — |

### `domain.comment` · layer: `domain`

Path: `src/domain/comment`
> Domain layer for the Comment domain class

| File | Classes |
|------|---------|
| `Comment.py` | `Resource`, `Comment`, `Role`, `Permission`, `State`, `CommentId`, `CommentCreatedEvent`, `CommentUpdatedEvent` |

### `dto.comment` · layer: `dto`

Path: `src/dto/comment`
> Dto layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_dto.py` | `CommentDto`, `PostDto`, `UserDto` |

### `repository.comment` · layer: `repository`

Path: `src/repository/comment`
> Repository layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_repository.py` | `CommentManagementAPI` |

### `orm.comment` · layer: `orm`

Path: `src/orm/comment`
> Orm layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_orm.py` | `CommentORM` |

### `infra.comment` · layer: `infra`

Path: `src/infra/comment`
> Infra layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_repo_impl.py` | `SQLAlchemyCommentRepository` |

### `service.comment` · layer: `service`

Path: `src/service/comment`
> Service layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_service.py` | `CommentService` |

### `api.comment` · layer: `api`

Path: `src/api/comment`
> Api layer for the Comment domain class

| File | Classes |
|------|---------|
| `comment_router.py` | `PostDetailPageUI` |

### `tests.unit.comment` · layer: `tests`

Path: `tests/unit/comment`
> Unit tests for Comment across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_comment_domain.py` | — |
| `test_comment_service.py` | — |
| `test_comment_api.py` | — |

### `domain.like` · layer: `domain`

Path: `src/domain/like`
> Domain layer for the Like domain class

| File | Classes |
|------|---------|
| `Like.py` | `Permission`, `State`, `Actor`, `Resource`, `Like`, `LikeId`, `LikeCreatedEvent`, `LikeUpdatedEvent` |

### `dto.like` · layer: `dto`

Path: `src/dto/like`
> Dto layer for the Like domain class

| File | Classes |
|------|---------|
| `like_dto.py` | `LikeRequest`, `LikeResponse` |

### `repository.like` · layer: `repository`

Path: `src/repository/like`
> Repository layer for the Like domain class

| File | Classes |
|------|---------|
| `like_repository.py` | `LikeApi`, `PostDatabase` |

### `orm.like` · layer: `orm`

Path: `src/orm/like`
> Orm layer for the Like domain class

| File | Classes |
|------|---------|
| `like_orm.py` | `LikeORM` |

### `infra.like` · layer: `infra`

Path: `src/infra/like`
> Infra layer for the Like domain class

| File | Classes |
|------|---------|
| `like_repo_impl.py` | `SQLAlchemyLikeRepository` |

### `service.like` · layer: `service`

Path: `src/service/like`
> Service layer for the Like domain class

| File | Classes |
|------|---------|
| `like_service.py` | `LikeService` |

### `api.like` · layer: `api`

Path: `src/api/like`
> Api layer for the Like domain class

| File | Classes |
|------|---------|
| `like_router.py` | `LikeController` |

### `tests.unit.like` · layer: `tests`

Path: `tests/unit/like`
> Unit tests for Like across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_like_domain.py` | — |
| `test_like_service.py` | — |
| `test_like_api.py` | — |

### `domain.notification` · layer: `domain`

Path: `src/domain/notification`
> Domain layer for the Notification domain class

| File | Classes |
|------|---------|
| `Notification.py` | `Notification`, `NotificationType`, `ChannelType`, `NotificationState`, `NotificationId`, `NotificationCreatedEvent`, `NotificationUpdatedEvent` |

### `dto.notification` · layer: `dto`

Path: `src/dto/notification`
> Dto layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_dto.py` | `LikeDTO`, `CommentDTO`, `NotificationDTO`, `NotificationPreferenceDTO` |

### `repository.notification` · layer: `repository`

Path: `src/repository/notification`
> Repository layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_repository.py` | `EmailNotificationAdapter`, `PushNotificationAdapter`, `InAppNotificationAdapter`, `PreferencesDatabaseAdapter`, `AuthenticationAdapter` |

### `orm.notification` · layer: `orm`

Path: `src/orm/notification`
> Orm layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_orm.py` | `NotificationORM` |

### `infra.notification` · layer: `infra`

Path: `src/infra/notification`
> Infra layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_repo_impl.py` | `SQLAlchemyNotificationRepository` |

### `service.notification` · layer: `service`

Path: `src/service/notification`
> Service layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_service.py` | `NotificationServiceAPI`, `UserPreferencesDatabase`, `AuthenticationSystem`, `NotificationService` |

### `api.notification` · layer: `api`

Path: `src/api/notification`
> Api layer for the Notification domain class

| File | Classes |
|------|---------|
| `notification_router.py` | `LikeController`, `CommentController`, `NotificationPreferenceController` |

### `tests.unit.notification` · layer: `tests`

Path: `tests/unit/notification`
> Unit tests for Notification across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_notification_domain.py` | — |
| `test_notification_service.py` | — |
| `test_notification_api.py` | — |

### `domain.profile` · layer: `domain`

Path: `src/domain/profile`
> Domain layer for the Profile domain class

| File | Classes |
|------|---------|
| `Profile.py` | `Profile`, `Photo`, `Biography`, `Resource`, `ProfileResource`, `Actor`, `Permission`, `State`, `Interface`, `AuthenticationStatus`, `Role`, `Visibility`, `AuditEntry`, `Operation`, `ProfileId`, `ProfileCreatedEvent`, `ProfileUpdatedEvent` |

### `dto.profile` · layer: `dto`

Path: `src/dto/profile`
> Dto layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_dto.py` | `ProfileCreateRequest`, `ProfileUpdateRequest`, `ProfileResponse` |

### `repository.profile` · layer: `repository`

Path: `src/repository/profile`
> Repository layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_repository.py` | `UserProfilesDatabase` |

### `orm.profile` · layer: `orm`

Path: `src/orm/profile`
> Orm layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_orm.py` | `ProfileORM` |

### `infra.profile` · layer: `infra`

Path: `src/infra/profile`
> Infra layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_repo_impl.py` | `SQLAlchemyProfileRepository` |

### `service.profile` · layer: `service`

Path: `src/service/profile`
> Service layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_service.py` | `REQ_USER_01` |

### `api.profile` · layer: `api`

Path: `src/api/profile`
> Api layer for the Profile domain class

| File | Classes |
|------|---------|
| `profile_router.py` | `Account_Settings_Page`, `ProfileSettingsAPI` |

### `tests.unit.profile` · layer: `tests`

Path: `tests/unit/profile`
> Unit tests for Profile across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_profile_domain.py` | — |
| `test_profile_service.py` | — |
| `test_profile_api.py` | — |

### `domain.report` · layer: `domain`

Path: `src/domain/report`
> Domain layer for the Report domain class

| File | Classes |
|------|---------|
| `Report.py` | `Report`, `ReportId`, `ReportCreatedEvent`, `ReportUpdatedEvent` |

### `dto.report` · layer: `dto`

Path: `src/dto/report`
> Dto layer for the Report domain class

| File | Classes |
|------|---------|
| `report_dto.py` | `ReportCreateRequest`, `ReportUpdateRequest`, `ReportResponse` |

### `repository.report` · layer: `repository`

Path: `src/repository/report`
> Repository layer for the Report domain class

| File | Classes |
|------|---------|
| `report_repository.py` | `ReportRepository` |

### `orm.report` · layer: `orm`

Path: `src/orm/report`
> Orm layer for the Report domain class

| File | Classes |
|------|---------|
| `report_orm.py` | `ReportORM` |

### `infra.report` · layer: `infra`

Path: `src/infra/report`
> Infra layer for the Report domain class

| File | Classes |
|------|---------|
| `report_repo_impl.py` | `SQLAlchemyReportRepository` |

### `service.report` · layer: `service`

Path: `src/service/report`
> Service layer for the Report domain class

| File | Classes |
|------|---------|
| `report_service.py` | `ReportService`, `ReportServiceImpl` |

### `api.report` · layer: `api`

Path: `src/api/report`
> Api layer for the Report domain class

| File | Classes |
|------|---------|
| `report_router.py` | `ReportRouter` |

### `tests.unit.report` · layer: `tests`

Path: `tests/unit/report`
> Unit tests for Report across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_report_domain.py` | — |
| `test_report_service.py` | — |
| `test_report_api.py` | — |

### `domain.verified_badge` · layer: `domain`

Path: `src/domain/verified_badge`
> Domain layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `VerifiedBadge.py` | `UserProfile`, `Admin`, `AuditEntry`, `Permission`, `AuditAction`, `VerifiedBadge`, `VerifiedBadgeId`, `VerifiedBadgeCreatedEvent`, `VerifiedBadgeUpdatedEvent` |

### `dto.verified_badge` · layer: `dto`

Path: `src/dto/verified_badge`
> Dto layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_dto.py` | `VerifiedBadgeCreateRequest`, `VerifiedBadgeUpdateRequest`, `VerifiedBadgeResponse` |

### `repository.verified_badge` · layer: `repository`

Path: `src/repository/verified_badge`
> Repository layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_repository.py` | `UserDatabase`, `AuditLoggingAPI` |

### `orm.verified_badge` · layer: `orm`

Path: `src/orm/verified_badge`
> Orm layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_orm.py` | `VerifiedBadgeORM` |

### `infra.verified_badge` · layer: `infra`

Path: `src/infra/verified_badge`
> Infra layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_repo_impl.py` | `SQLAlchemyVerifiedBadgeRepository` |

### `service.verified_badge` · layer: `service`

Path: `src/service/verified_badge`
> Service layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_service.py` | `BadgeManagementService`, `BadgeOperationRequest` |

### `api.verified_badge` · layer: `api`

Path: `src/api/verified_badge`
> Api layer for the VerifiedBadge domain class

| File | Classes |
|------|---------|
| `verified_badge_router.py` | `AdminUserManagementInterface`, `AdminUserManagementController` |

### `tests.unit.verified_badge` · layer: `tests`

Path: `tests/unit/verified_badge`
> Unit tests for VerifiedBadge across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_verified_badge_domain.py` | — |
| `test_verified_badge_service.py` | — |
| `test_verified_badge_api.py` | — |

### `config.settings` · layer: `config`

Path: `src/config`
> Application settings, environment variables, dependency injection

| File | Classes |
|------|---------|
| `settings.py` | `Settings` |
| `dependencies.py` | `Container` |
| `database.py` | — |
| `logging.py` | — |

### `docs.api_and_deployment` · layer: `docs`

Path: `docs`
> OpenAPI documentation, admin guide, multi-city config, deployment runbook

*(no files specified)*

### `tests.integration` · layer: `tests`

Path: `tests/integration`
> End-to-end and cross-service integration tests

| File | Classes |
|------|---------|
| `test_user_flow.py` | — |
| `test_post_flow.py` | — |
| `test_notification_preference_flow.py` | — |
| `test_verified_badge_flow.py` | — |
| `test_group_flow.py` | — |
| `test_profile_flow.py` | — |
| `test_friendship_flow.py` | — |
| `test_audit_log_flow.py` | — |
| `test_block_flow.py` | — |
| `test_follow_flow.py` | — |
| `test_message_flow.py` | — |
| `test_like_flow.py` | — |
| `test_bookmark_flow.py` | — |
| `test_report_flow.py` | — |
| `test_comment_flow.py` | — |
| `test_group_membership_flow.py` | — |
| `test_notification_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #157 — User Registration with Email Verification

**As a** new user  
**I need** to register an account
**So that** I can securely access the platform  

### Details and Assumptions
* The user is new and does not have an existing account.  

### Acceptance Criteria

```gherkin
Given I am a new user on the registration page
When I submit my registration details with a valid email address
Then I create my account
```

**UML class diagram:** `experiments/project_16/class_diagram_157.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `AccountStatus`, `Actor`, `EmailConfirmation`, `Interface`, `InterfaceKind`, `Permission`, `REQ_REG_01`, `Resource`, `State`, `UserAccount` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/repository/user/user_repository.py` | `EmailNotificationSystem`, `EmailValidator`, `RegistrationPage`, `UserDatabase` |
| `src/repository/verified_badge/verified_badge_repository.py` | `UserDatabase` |

---

### Task #158 — Profile Creation with Photo and Bio

**As a** registered user
**I need** create a profile with a profile photo and a short biography
**So that** I can personalize my account and share information about myself

### Details and Assumptions
* Profile creation requires a valid photo (JPEG, PNG) up to 2 MB and a biography up to 500 characters.
* Profile can be created from the account settings page.

### Acceptance Criteria

```gherkin
Given I am a registered user
When I upload a valid photo and enter a biography under 500 characters
Then my profile is created and displayed successfully
```

**UML class diagram:** `experiments/project_16/class_diagram_158.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/profile/profile_router.py` | `Account_Settings_Page` |
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Biography`, `Interface`, `Permission`, `Photo`, `Profile`, `ProfileResource`, `Resource`, `State` |
| `src/domain/user/User.py` | `Interface`, `Permission`, `Resource`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/service/profile/profile_service.py` | `REQ_USER_01` |

---

### Task #159 — Text Post Creation with Image Upload

**As a** user
**I need** to create a text post and optionally upload images
**So that** I can share content with others

### Details and Assumptions
* The user can write text content for the post.
* The user can optionally attach one or more images to the post.
* The post will be visible to other users.

### Acceptance Criteria

```gherkin
Given I am a logged-in user
When I create a new post with text and optionally upload images
Then the post is saved and shared with others
```

**UML class diagram:** `experiments/project_16/class_diagram_159.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/post/post_router.py` | `PostCreationAPI` |
| `src/domain/audit_log/AuditLog.py` | `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Role` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/group/Group.py` | `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `Permission`, `Role` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Image`, `Permission`, `Post`, `PostState`, `Role` |
| `src/domain/profile/Profile.py` | `Permission`, `Role` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/post/post_dto.py` | `CreatePostRequest`, `CreatePostResponse` |
| `src/repository/post/post_repository.py` | `ContentDatabase`, `ImageStorageService` |

---

### Task #160 — Post Like/Unlike with Count Display

**As a** user
**I need** to like or unlike a post and see the total number of likes displayed
**So that** I can engage with content and view its popularity

### Details and Assumptions
* The post has a like/unlike button
* The total like count updates immediately after interaction
* Users can toggle between like and unlike

### Acceptance Criteria

```gherkin
Given a post with an initial like count
When I click the like button
Then the like count increases by 1
And the button changes to an unliked state

Given a post I have already liked
When I click the unlike button
Then the like count decreases by 1
And the button changes back to a liked state
```

**UML class diagram:** `experiments/project_16/class_diagram_160.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/like/like_router.py` | `LikeController` |
| `src/api/notification/notification_router.py` | `LikeController` |
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Like`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post` |
| `src/domain/profile/Profile.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `Resource`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/like/like_dto.py` | `LikeRequest`, `LikeResponse` |
| `src/repository/like/like_repository.py` | `LikeApi` |
| `src/service/like/like_service.py` | `LikeService` |

---

### Task #161 — Flat Comment Creation and Management

**As a** user
**I need** add comments on posts and manage my own comments (edit/delete)
**So that** I can engage with content and control my contributions

### Details and Assumptions
* Comments are flat (no nesting).

### Acceptance Criteria

```gherkin
Given I am on a post detail page
When I write a comment and submit
Then the comment appears on the post

Given I have a comment on a post
When I edit my comment
Then the comment content is updated

Given I have a comment on a post
When I delete my comment
Then the comment is removed from the post
```

**UML class diagram:** `experiments/project_16/class_diagram_161.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/comment/comment_router.py` | `PostDetailPageUI` |
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Comment`, `Permission`, `Resource`, `Role`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission`, `Role` |
| `src/domain/like/Like.py` | `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post`, `Role` |
| `src/domain/profile/Profile.py` | `Permission`, `Resource`, `Role`, `State` |
| `src/domain/user/User.py` | `Permission`, `Resource`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/comment/comment_dto.py` | `CommentDto`, `PostDto`, `UserDto` |
| `src/repository/comment/comment_repository.py` | `CommentManagementAPI` |
| `src/service/comment/comment_service.py` | `CommentService` |

---

### Task #162 — Chronological News Feed from Friends

**As a** user
**I need** to see a news feed showing posts from my friends in chronological order
**So that** I can view my friends' recent activities without missing any updates

### Details and Assumptions
* The feed displays only posts from friends of the user.
* Chronological order means posts are sorted by creation time, with the newest appearing first.
* Posts may include text, images, or other media as supported by the system.

### Acceptance Criteria

```gherkin
Given the user is logged in and has friends with posts
When the user navigates to the news feed page
Then the user sees a list of posts from friends sorted by time (newest first)
```

**UML class diagram:** `experiments/project_16/class_diagram_162.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Role` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/friendship/Friendship.py` | `Friendship` |
| `src/domain/group/Group.py` | `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `Permission`, `Role` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post`, `Role` |
| `src/domain/profile/Profile.py` | `Permission`, `Role` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |

---

### Task #163 — Friend Request Send and Accept/Reject

**As a** user
**I need** to send friend requests to other users and accept or reject incoming requests
**So that** I can connect with others and manage my network

### Details and Assumptions
* Sending a friend request notifies the recipient
* Users can accept or reject incoming requests
* Accepted requests create a mutual friendship

### Acceptance Criteria

```gherkin
Given I am logged in
When I send a friend request to another user
Then the recipient gets notified of the pending request

Given I have a pending friend request
When I accept it
Then we become friends and the sender is notified

Given I have a pending friend request
When I reject it
Then the request is removed and the sender is notified
```

**UML class diagram:** `experiments/project_16/class_diagram_163.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/friendship/Friendship.py` | `FriendRequest`, `FriendRequestStatus`, `Friendship`, `NotificationType`, `OnlineStatus` |
| `src/domain/notification/Notification.py` | `Notification`, `NotificationType` |
| `src/domain/user/User.py` | `User` |

---

### Task #164 — Follow/Unfollow Users with Counts

**As a** user
**I need** to follow or unfollow other users and see the follower/following counts on their profiles
**So that** I can manage my connections and understand their social influence

### Details and Assumptions
* The feature includes both following and unfollowing actions.
* Follower and following counts are displayed on the user's profile page.
* Counts update in real-time or after a page refresh.
* The user must already be logged in to perform follow/unfollow actions.

### Acceptance Criteria

```gherkin
Given I am logged in and viewing another user's profile
When I click the "Follow" button
Then the button changes to "Unfollow" and the follower count on that profile increases by 1
And the user I followed sees a new follower notification (if applicable)

Given I am currently following a user
When I click the "Unfollow" button on their profile
Then the button changes to "Follow" and the follower count on that profile decreases by 1
```

**UML class diagram:** `experiments/project_16/class_diagram_164.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/follow/follow_router.py` | `FollowUnfollowController` |
| `src/domain/audit_log/AuditLog.py` | `Permission`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State`, `UserProfile` |
| `src/domain/group/Group.py` | `Actor`, `Permission`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `State` |
| `src/domain/message/Message.py` | `Actor`, `Permission`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission`, `UserProfile` |
| `src/dto/follow/follow_dto.py` | `FollowRequest`, `FollowResponse`, `UnfollowRequest` |
| `src/repository/follow/follow_repository.py` | `FollowUnfollowAPI`, `UserProfileDatabase` |
| `src/service/follow/follow_service.py` | `FollowUnfollowService` |

---

### Task #165 — Group Creation with Public/Private Flag

**As a** user
**I need** to create a group and set its visibility as public or private
**So that** I can control who can view or join the group

### Details and Assumptions
* The group creation form includes a visibility selection (public/private).
* Public groups are visible and joinable by anyone; private groups require approval or invitation.

### Acceptance Criteria

```gherkin
Given a user is on the group creation page
When the user fills in group details and selects a visibility (public or private)
Then the group is created with the specified visibility
```

**UML class diagram:** `experiments/project_16/class_diagram_165.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/group/group_router.py` | `GroupController` |
| `src/domain/audit_log/AuditLog.py` | `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `Group`, `GroupName`, `IfaceKind`, `Interface`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Actor`, `Interface`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/group/group_dto.py` | `CreateGroupRequest`, `CreateGroupResponse` |
| `src/repository/group/group_repository.py` | `GroupCreationAPI`, `GroupDB` |
| `src/service/group/group_service.py` | `GroupCreationService` |

---

### Task #166 — Private Group Join Request Approval

**As a** group owner/admin
**I need** to review and approve/reject join requests for private groups
**So that** only approved members can join the private group

### Details and Assumptions
* Private groups have a join request system where users can request to join.
* Group owners/admins have the ability to see pending requests.
* Approving a request adds the user to the group; rejecting removes or denies the request.
* The input text is clear about the feature need.

### Acceptance Criteria

```gherkin
Given a private group with pending join requests
When the group owner/admin accesses the join requests management section
Then they can see a list of pending requests with user details
And for each request, they can choose to approve or reject
And after approval, the requesting user becomes a member of the group
And after rejection, the request is removed and the user is not added
```

**UML class diagram:** `experiments/project_16/class_diagram_166.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Role` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/group/Group.py` | `Group`, `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `GroupMembership`, `JoinRequest`, `JoinRequestStatus`, `Permission`, `Role` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Role` |
| `src/domain/profile/Profile.py` | `Permission`, `Role` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/repository/group_membership/group_membership_repository.py` | `GroupAPI`, `JoinRequestManagementUI`, `JoinRequestsDatabase` |

---

### Task #167 — Group-Specific Feed Display

**As a** group member
**I need** to see a feed of posts only from the groups I belong to
**So that** I can stay updated with content from my groups without unrelated posts

### Details and Assumptions
* The user is authenticated and a member of one or more groups.
* Each post is associated with a specific group.
* The feed is filtered to show only posts from groups the user belongs to.
* Groups are distinct entities with their own posts.
* The feed may be sorted by time or relevance.

### Acceptance Criteria

```gherkin
Given I am a group member logged into the system
And I belong to multiple groups
When I view the group feed
Then I see only posts from the groups I belong to
And I do not see posts from groups I am not a member of
```

**UML class diagram:** `experiments/project_16/class_diagram_167.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Group`, `IfaceKind`, `Permission`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission`, `State` |
| `src/domain/message/Message.py` | `IfaceKind`, `Permission`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Permission`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |

---

### Task #168 — One-on-One Direct Messaging

**As a** user
**I need** to send and receive private messages directly with another user
**So that** I can communicate one-on-one with other users

### Details and Assumptions
* Users can initiate a private conversation with any other user.
* Messages are delivered instantly and only visible to the two participants.
* Users can view their message history.

### Acceptance Criteria

```gherkin
Given I am a logged-in user
When I navigate to a user's profile and click "Send Message"
Then I can compose and send a private message to that user

Given I have received a private message from another user
When I open my inbox
Then I can read the message and reply directly to the sender
```

**UML class diagram:** `experiments/project_16/class_diagram_168.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `IfaceKind`, `Interface`, `Message_Service_API`, `Permission`, `Resource`, `State`, `User_Database` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/service/message/message_service.py` | `REQ_PRIV_MES_01`, `ReceiveMessageOperation`, `ReplyToMessageOperation`, `SendMessageOperation` |

---

### Task #169 — Notifications for Likes and Comments

**As a** user
**I need** to receive notifications when someone likes or comments on my post
**So that** I can stay updated on interactions with my post

### Details and Assumptions
* Only likes and comments trigger notifications; other interactions (e.g., shares, saves) are not included.
* Notifications may be delivered via email, push, or in-app, but the exact channel is not specified.
* The user has enabled notifications for post interactions (default assumption).

### Acceptance Criteria

```gherkin
Given I am a logged-in user with a published post
When another user likes my post
Then I receive a notification that someone liked my post

Given I am a logged-in user with a published post
When another user comments on my post
Then I receive a notification that someone commented on my post

Given I am a logged-in user with a published post
When I have disabled notifications for that post
And another user likes or comments on my post
Then I do not receive any notification
```

**UML class diagram:** `experiments/project_16/class_diagram_169.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/like/like_router.py` | `LikeController` |
| `src/api/notification/notification_router.py` | `CommentController`, `LikeController`, `NotificationPreferenceController` |
| `src/domain/comment/Comment.py` | `Comment` |
| `src/domain/friendship/Friendship.py` | `NotificationType` |
| `src/domain/like/Like.py` | `Like` |
| `src/domain/notification/Notification.py` | `ChannelType`, `Notification`, `NotificationState`, `NotificationType` |
| `src/domain/notification_preference/NotificationPreference.py` | `NotificationPreference` |
| `src/domain/post/Post.py` | `Post` |
| `src/domain/user/User.py` | `User` |
| `src/dto/notification/notification_dto.py` | `CommentDTO`, `LikeDTO`, `NotificationDTO`, `NotificationPreferenceDTO` |
| `src/dto/notification_preference/notification_preference_dto.py` | `NotificationPreferenceDTO` |
| `src/repository/notification/notification_repository.py` | `AuthenticationAdapter`, `EmailNotificationAdapter`, `InAppNotificationAdapter`, `PreferencesDatabaseAdapter`, `PushNotificationAdapter` |
| `src/service/notification/notification_service.py` | `AuthenticationSystem`, `NotificationService`, `NotificationServiceAPI`, `UserPreferencesDatabase` |

---

### Task #170 — Keyword Search Across Users and Posts

**As a** user
**I need** to search across all users and posts using keywords
**So that** I can quickly find relevant users or content

### Details and Assumptions
* The search should support keywords for both user names/descriptions and post content.
* The search returns a combined list of matching users and posts, possibly with type labels.

### Acceptance Criteria

```gherkin
Given I am logged into the system
When I enter a keyword in the search bar
Then I see a list of users and posts that match the keyword
```

**UML class diagram:** `experiments/project_16/class_diagram_170.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/repository/like/like_repository.py` | `PostDatabase` |
| `src/repository/user/user_repository.py` | `UserDatabase` |
| `src/repository/verified_badge/verified_badge_repository.py` | `UserDatabase` |

---

### Task #171 — Bookmark Posts to Saved List

**As a** user
**I need** to bookmark posts and view them later in a saved list
**So that** I can easily access and revisit posts I find interesting

### Details and Assumptions
* The system should provide a way to mark a post as bookmarked
* The saved list should contain all bookmarked posts
* The saved list should be accessible from the user's profile or a dedicated menu

### Acceptance Criteria

```gherkin
Given I am logged in as a user
When I bookmark a post
Then the post should be added to my saved list

Given I have bookmarked posts
When I navigate to my saved list
Then I should see all my bookmarked posts
```

**UML class diagram:** `experiments/project_16/class_diagram_171.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/bookmark/bookmark_router.py` | `IUserUI` |
| `src/domain/audit_log/AuditLog.py` | `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Bookmark`, `LoginStatus`, `Permission`, `SavedList` |
| `src/domain/comment/Comment.py` | `Permission` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/group/Group.py` | `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post` |
| `src/domain/profile/Profile.py` | `Permission` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/bookmark/bookmark_dto.py` | `BookmarkRequest`, `BookmarkResponse`, `SavedListResponse` |
| `src/repository/bookmark/bookmark_repository.py` | `IUserDatabase` |
| `src/service/bookmark/bookmark_service.py` | `BookmarkService` |

---

### Task #172 — Report Post with Reason Dropdown

**As a** user
**I need** to report a post by selecting a reason from a dropdown menu
**So that** inappropriate content can be flagged and reviewed

### Details and Assumptions
* The user must be logged in to report a post.
* A dropdown menu with predefined report reasons is provided.
* The user selects a reason and confirms the report.

### Acceptance Criteria

```gherkin
Given a user is viewing a post
When they click "Report" and select a reason from the dropdown menu
Then the post is flagged for review and a confirmation message is shown
```

*(No UML class diagram found for this task)*

---

### Task #173 — Admin Panel for Reported Content

**As a** admin
**I need** a panel to review reported content and take appropriate actions (warn, hide, delete)
**So that** I can moderate content effectively

### Details and Assumptions
* The panel should list reported content with details.
* Actions include warn, hide, and delete.
* Admin must be authenticated.

### Acceptance Criteria

```gherkin
Given I am logged in as an admin
When I navigate to the reported content panel
Then I see a list of reported items with options to warn, hide, or delete
```

**UML class diagram:** `experiments/project_16/class_diagram_173.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |

---

### Task #174 — Profile Privacy Public/Private Toggle

**As a** user
**I need** to toggle my profile visibility between public and private
**So that** I can control who sees my profile

### Details and Assumptions
* The profile visibility setting can be changed at any time.
* There are two states: public (visible to everyone) and private (visible only to the user or authorized connections).

### Acceptance Criteria

```gherkin
Given I am on my profile settings page
When I toggle the profile visibility option
Then my profile visibility changes between public and private accordingly
```

**UML class diagram:** `experiments/project_16/class_diagram_174.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/profile/profile_router.py` | `ProfileSettingsAPI` |
| `src/domain/audit_log/AuditLog.py` | `Operation`, `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Role` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/group/Group.py` | `Operation`, `Permission`, `Visibility` |
| `src/domain/group_membership/GroupMembership.py` | `Permission`, `Role` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Role` |
| `src/domain/profile/Profile.py` | `AuditEntry`, `AuthenticationStatus`, `Operation`, `Permission`, `Profile`, `Role`, `Visibility` |
| `src/domain/user/User.py` | `Operation`, `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `AuditEntry`, `Permission` |
| `src/repository/profile/profile_repository.py` | `UserProfilesDatabase` |

---

### Task #175 — Block User to Hide Content and Messages

**As a** user
**I need** to block another user
**So that** their posts and messages are hidden from me

### Details and Assumptions
* Blocking is performed via a user profile or settings option.
* Once blocked, all existing and future posts and messages from the blocked user are hidden.
* The blocked user is not notified of the block.
* The blocking can be undone through a "blocked users" management list.

### Acceptance Criteria

```gherkin
Given I am a logged-in user
And I have a list of posts and messages from user "Alice"
When I block user "Alice"
Then all posts and messages from "Alice" are hidden from my view
And I no longer receive new messages or see new posts from "Alice"
```

**UML class diagram:** `experiments/project_16/class_diagram_175.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `State` |
| `src/domain/block/Block.py` | `BlockRecord`, `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Permission`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission`, `State` |
| `src/domain/message/Message.py` | `Message`, `Permission`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post` |
| `src/domain/profile/Profile.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Permission`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/repository/block/block_repository.py` | `MessagesDatabase`, `NotificationSystem`, `PostsDatabase`, `UserProfileAPI` |

---

### Task #176 — Notification Preference Toggles per Category

**As a** user
**I need** to enable or disable notifications per category (e.g., likes, comments, friend requests)
**So that** I can control which notifications I receive

### Details and Assumptions
* The system supports notification categories such as likes, comments, and friend requests.
* Each category has a toggle (on/off).
* Changes take effect immediately.

### Acceptance Criteria

```gherkin
Given I am logged into the application
When I navigate to the notification settings
Then I see a list of notification categories with toggles

Given I am on the notification settings page
When I toggle off "likes" notifications
Then I no longer receive notifications for likes

Given I am on the notification settings page
When I toggle on "comments" notifications
Then I receive notifications for comments
```

**UML class diagram:** `experiments/project_16/class_diagram_176.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/notification_preference/notification_preference_router.py` | `NotificationSettingsController` |
| `src/domain/audit_log/AuditLog.py` | `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission` |
| `src/domain/follow/Follow.py` | `Permission` |
| `src/domain/group/Group.py` | `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `NotificationCategory`, `NotificationPreference`, `Permission`, `UserState` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Permission` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/notification/notification_dto.py` | `NotificationPreferenceDTO` |
| `src/dto/notification_preference/notification_preference_dto.py` | `NotificationPreferenceDTO` |
| `src/repository/notification_preference/notification_preference_repository.py` | `NotificationPreferenceRepository` |
| `src/service/notification_preference/notification_preference_service.py` | `NotificationSettingsService` |

---

### Task #177 — Admin Verified Badge Grant/Revoke

**As a** admin
**I need** to grant or revoke verified badges on user profiles
**So that** I can manage the verification status of users to ensure credibility

### Details and Assumptions
* The admin has access to a user management interface.
* Verified badges are displayed on user profiles.
* Granting a badge confirms the user's identity or status.
* Revoking a badge removes the verification indicator.

### Acceptance Criteria

```gherkin
Given I am an authenticated admin with user management privileges
When I select a user profile and choose to grant a verified badge
Then the user's profile displays a verified badge

Given I am an authenticated admin with user management privileges
When I select a user profile that currently has a verified badge and choose to revoke it
Then the verified badge is removed from the user's profile
```

**UML class diagram:** `experiments/project_16/class_diagram_177.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/verified_badge/verified_badge_router.py` | `AdminUserManagementController`, `AdminUserManagementInterface` |
| `src/domain/audit_log/AuditLog.py` | `Admin`, `Permission` |
| `src/domain/block/Block.py` | `Permission` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission` |
| `src/domain/follow/Follow.py` | `Permission`, `UserProfile` |
| `src/domain/group/Group.py` | `Permission` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission` |
| `src/domain/message/Message.py` | `Permission` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `AuditEntry`, `Permission` |
| `src/domain/user/User.py` | `Permission` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Admin`, `AuditAction`, `AuditEntry`, `Permission`, `UserProfile` |
| `src/repository/user/user_repository.py` | `UserDatabase` |
| `src/repository/verified_badge/verified_badge_repository.py` | `AuditLoggingAPI`, `UserDatabase` |
| `src/service/verified_badge/verified_badge_service.py` | `BadgeManagementService` |

---

### Task #178 — User Post History and Account Settings

**As a** user
**I need** to view my own post history and manage account settings (change password, email, delete account)
**So that** I can control my account and review my posts

### Details and Assumptions
* User is logged in
* Post history shows list of previous posts with timestamps
* Account settings include change password, change email, and delete account options
* Deleting account may be irreversible

### Acceptance Criteria

```gherkin
Scenario: View post history
Given I am logged in as a user
When I navigate to my profile page
Then I see a list of my previous posts

Scenario: Manage account settings
Given I am logged in as a user
When I access account settings
Then I can change my password, change my email, or delete my account
```

**UML class diagram:** `experiments/project_16/class_diagram_178.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Permission`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission`, `State` |
| `src/domain/message/Message.py` | `Permission`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Post` |
| `src/domain/profile/Profile.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Permission`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |

---

### Task #179 — Pagination on Feeds and Search Results

**As a** user
**I need** paginated results when browsing feeds or search results
**So that** to avoid long loading times

### Details and Assumptions
* Pagination applies to both feeds and search result pages.
* Each page shows a reasonable number of items (e.g., 20).
* Users can navigate between pages using next/previous links or page numbers.

### Acceptance Criteria

```gherkin
Given I am browsing a feed or viewing search results
When I scroll to the bottom of the current page
Then I see a "Load More" button or page navigation controls
And only the first page of results is loaded initially
```

**UML class diagram:** `experiments/project_16/class_diagram_179.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `Role`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission`, `Role` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission`, `Role` |
| `src/domain/profile/Profile.py` | `Actor`, `Interface`, `Permission`, `Resource`, `Role`, `State` |
| `src/domain/user/User.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |

---

### Task #180 — Account Soft-Deletion with Deleted Flag

**As a** user  
**I need** to soft-delete my account  
**So that** my data is preserved for a grace period while my account is marked as deleted  

### Details and Assumptions
* Soft-delete means the account is not permanently removed immediately.
* A grace period allows for potential account recovery or data restoration.
* The system retains the account data during this period.

### Acceptance Criteria

```gherkin
Given I have an active account
When I request to soft-delete my account
Then my account is marked as deleted
And my data is preserved for a grace period
```

**UML class diagram:** `experiments/project_16/class_diagram_180.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Operation`, `Permission`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `State` |
| `src/domain/follow/Follow.py` | `Actor`, `Permission`, `State` |
| `src/domain/group/Group.py` | `Actor`, `Operation`, `Permission`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Actor`, `Permission`, `State` |
| `src/domain/message/Message.py` | `Actor`, `Permission`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Actor`, `Operation`, `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `InterfaceKind`, `Operation`, `Permission`, `State`, `UserAccount`, `UserAccountStatus` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Permission` |
| `src/dto/user/user_dto.py` | `AccountStatusResponse`, `SoftDeleteRequest` |
| `src/repository/user/user_repository.py` | `AccountManagementService` |

---

### Task #181 — Admin Role Enforcement with Action Logging

**As a** admin
**I need** all admin actions (e.g., banning, warning) to be logged
**So that** actions can be audited

### Details and Assumptions
* Admin actions include banning and warning users.
* Logs should be stored persistently and be accessible for review.

### Acceptance Criteria

```gherkin
Given an admin performs an action (e.g., banning or warning a user)
When the action is completed
Then the action is recorded in the audit log with details (admin ID, action type, timestamp, target user)
```

**UML class diagram:** `experiments/project_16/class_diagram_181.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_log/AuditLog.py` | `Admin`, `AuditLog`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/block/Block.py` | `Permission`, `State` |
| `src/domain/bookmark/Bookmark.py` | `Permission` |
| `src/domain/comment/Comment.py` | `Permission`, `Resource`, `State` |
| `src/domain/follow/Follow.py` | `Permission`, `State` |
| `src/domain/group/Group.py` | `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/group_membership/GroupMembership.py` | `Permission` |
| `src/domain/like/Like.py` | `Permission`, `Resource`, `State` |
| `src/domain/message/Message.py` | `Permission`, `Resource`, `State` |
| `src/domain/notification_preference/NotificationPreference.py` | `Permission` |
| `src/domain/post/Post.py` | `Permission` |
| `src/domain/profile/Profile.py` | `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/user/User.py` | `Operation`, `Permission`, `Resource`, `State`, `User` |
| `src/domain/verified_badge/VerifiedBadge.py` | `Admin`, `Permission` |

---
