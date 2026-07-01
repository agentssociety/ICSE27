from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.audit_entry.audit_entry_repo_impl import SQLAlchemyAuditEntryRepository
from src.infra.audit_log.audit_log_repo_impl import SQLAlchemyAuditLogRepository
from src.infra.biography.biography_repo_impl import SQLAlchemyBiographyRepository
from src.infra.block.block_repo_impl import SQLAlchemyBlockRepository
from src.infra.block_record.block_record_repo_impl import SQLAlchemyBlockRecordRepository
from src.infra.bookmark.bookmark_repo_impl import SQLAlchemyBookmarkRepository
from src.infra.comment.comment_repo_impl import SQLAlchemyCommentRepository
from src.infra.friend_request.friend_request_repo_impl import SQLAlchemyFriendRequestRepository
from src.infra.friendship.friendship_repo_impl import SQLAlchemyFriendshipRepository
from src.infra.group.group_repo_impl import SQLAlchemyGroupRepository
from src.infra.group_membership.group_membership_repo_impl import SQLAlchemyGroupMembershipRepository
from src.infra.join_request.join_request_repo_impl import SQLAlchemyJoinRequestRepository
from src.infra.like.like_repo_impl import SQLAlchemyLikeRepository
from src.infra.message.message_repo_impl import SQLAlchemyMessageRepository
from src.infra.message_service_api.message_service_api_repo_impl import SQLAlchemyMessage_Service_APIRepository
from src.infra.notification.notification_repo_impl import SQLAlchemyNotificationRepository
from src.infra.notification_preference.notification_preference_repo_impl import SQLAlchemyNotificationPreferenceRepository
from src.infra.operation.operation_repo_impl import SQLAlchemyOperationRepository
from src.infra.photo.photo_repo_impl import SQLAlchemyPhotoRepository
from src.infra.profile.profile_repo_impl import SQLAlchemyProfileRepository
from src.infra.report.report_repo_impl import SQLAlchemyReportRepository
from src.infra.role.role_repo_impl import SQLAlchemyRoleRepository
from src.infra.saved_list.saved_list_repo_impl import SQLAlchemySavedListRepository
from src.infra.user_profile.user_profile_repo_impl import SQLAlchemyUserProfileRepository
from src.infra.user_database.user_database_repo_impl import SQLAlchemyUser_DatabaseRepository
from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
from src.infra.verified_badge.verified_badge_repo_impl import SQLAlchemyVerifiedBadgeRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_audit_entry_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuditEntryRepository:
    return SQLAlchemyAuditEntryRepository(db)

def get_audit_log_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogRepository:
    return SQLAlchemyAuditLogRepository(db)

def get_biography_repository(db: Session = Depends(get_db)) -> SQLAlchemyBiographyRepository:
    return SQLAlchemyBiographyRepository(db)

def get_block_repository(db: Session = Depends(get_db)) -> SQLAlchemyBlockRepository:
    return SQLAlchemyBlockRepository(db)

def get_block_record_repository(db: Session = Depends(get_db)) -> SQLAlchemyBlockRecordRepository:
    return SQLAlchemyBlockRecordRepository(db)

def get_bookmark_repository(db: Session = Depends(get_db)) -> SQLAlchemyBookmarkRepository:
    return SQLAlchemyBookmarkRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> SQLAlchemyCommentRepository:
    return SQLAlchemyCommentRepository(db)

def get_friend_request_repository(db: Session = Depends(get_db)) -> SQLAlchemyFriendRequestRepository:
    return SQLAlchemyFriendRequestRepository(db)

def get_friendship_repository(db: Session = Depends(get_db)) -> SQLAlchemyFriendshipRepository:
    return SQLAlchemyFriendshipRepository(db)

def get_group_repository(db: Session = Depends(get_db)) -> SQLAlchemyGroupRepository:
    return SQLAlchemyGroupRepository(db)

def get_group_membership_repository(db: Session = Depends(get_db)) -> SQLAlchemyGroupMembershipRepository:
    return SQLAlchemyGroupMembershipRepository(db)

def get_join_request_repository(db: Session = Depends(get_db)) -> SQLAlchemyJoinRequestRepository:
    return SQLAlchemyJoinRequestRepository(db)

def get_like_repository(db: Session = Depends(get_db)) -> SQLAlchemyLikeRepository:
    return SQLAlchemyLikeRepository(db)

def get_message_repository(db: Session = Depends(get_db)) -> SQLAlchemyMessageRepository:
    return SQLAlchemyMessageRepository(db)

def get_message_service_api_repository(db: Session = Depends(get_db)) -> SQLAlchemyMessage_Service_APIRepository:
    return SQLAlchemyMessage_Service_APIRepository(db)

def get_notification_repository(db: Session = Depends(get_db)) -> SQLAlchemyNotificationRepository:
    return SQLAlchemyNotificationRepository(db)

def get_notification_preference_repository(db: Session = Depends(get_db)) -> SQLAlchemyNotificationPreferenceRepository:
    return SQLAlchemyNotificationPreferenceRepository(db)

def get_operation_repository(db: Session = Depends(get_db)) -> SQLAlchemyOperationRepository:
    return SQLAlchemyOperationRepository(db)

def get_photo_repository(db: Session = Depends(get_db)) -> SQLAlchemyPhotoRepository:
    return SQLAlchemyPhotoRepository(db)

def get_profile_repository(db: Session = Depends(get_db)) -> SQLAlchemyProfileRepository:
    return SQLAlchemyProfileRepository(db)

def get_report_repository(db: Session = Depends(get_db)) -> SQLAlchemyReportRepository:
    return SQLAlchemyReportRepository(db)

def get_role_repository(db: Session = Depends(get_db)) -> SQLAlchemyRoleRepository:
    return SQLAlchemyRoleRepository(db)

def get_saved_list_repository(db: Session = Depends(get_db)) -> SQLAlchemySavedListRepository:
    return SQLAlchemySavedListRepository(db)

def get_user_profile_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserProfileRepository:
    return SQLAlchemyUserProfileRepository(db)

def get_user_database_repository(db: Session = Depends(get_db)) -> SQLAlchemyUser_DatabaseRepository:
    return SQLAlchemyUser_DatabaseRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)

def get_verified_badge_repository(db: Session = Depends(get_db)) -> SQLAlchemyVerifiedBadgeRepository:
    return SQLAlchemyVerifiedBadgeRepository(db)


class Container:
    @staticmethod
    def get_user_service(db: Session = Depends(get_db)) -> object:
        from src.service.user.user_service import UserServiceImpl
        from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
        repo = SQLAlchemyUserRepository(db)
        return UserServiceImpl(repo)
