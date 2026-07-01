from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.database import create_tables
from src.config.settings import settings
from src.api.actor.actor_router import router as actor_router
from src.api.audit_entry.audit_entry_router import router as audit_entry_router
from src.api.audit_log.audit_log_router import router as audit_log_router
from src.api.biography.biography_router import router as biography_router
from src.api.block.block_router import router as block_router
from src.api.block_record.block_record_router import router as block_record_router
from src.api.bookmark.bookmark_router import router as bookmark_router
from src.api.comment.comment_router import router as comment_router
from src.api.follow.follow_router import router as follow_router
from src.api.friend_request.friend_request_router import router as friend_request_router
from src.api.friendship.friendship_router import router as friendship_router
from src.api.group.group_router import router as group_router
from src.api.group_membership.group_membership_router import router as group_membership_router
from src.api.join_request.join_request_router import router as join_request_router
from src.api.like.like_router import router as like_router
from src.api.message.message_router import router as message_router
from src.api.message_service_api.message_service_api_router import router as message_service_api_router
from src.api.notification.notification_router import router as notification_router
from src.api.notification_preference.notification_preference_router import router as notification_preference_router
from src.api.operation.operation_router import router as operation_router
from src.api.photo.photo_router import router as photo_router
from src.api.post.post_router import router as post_router
from src.api.profile.profile_router import router as profile_router
from src.api.report.report_router import router as report_router
from src.api.role.role_router import router as role_router
from src.api.saved_list.saved_list_router import router as saved_list_router
from src.api.user_profile.user_profile_router import router as user_profile_router
from src.api.user_database.user_database_router import router as user_database_router
from src.api.user.user_router import router as user_router
from src.api.verified_badge.verified_badge_router import router as verified_badge_router

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        _log.info("Database tables created / verified.")
    except Exception as exc:
        _log.warning("DB unavailable at startup (will retry per request): %s", exc)
    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Auto-generated API",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actor_router, prefix="/actors", tags=["Actor"])
app.include_router(audit_entry_router, prefix="/audit_entrys", tags=["AuditEntry"])
app.include_router(audit_log_router, prefix="/audit_logs", tags=["AuditLog"])
app.include_router(biography_router, prefix="/biographys", tags=["Biography"])
app.include_router(block_router, prefix="/blocks", tags=["Block"])
app.include_router(block_record_router, prefix="/block_records", tags=["BlockRecord"])
app.include_router(bookmark_router, prefix="/bookmarks", tags=["Bookmark"])
app.include_router(comment_router, prefix="/comments", tags=["Comment"])
app.include_router(follow_router, tags=["Follow"])
app.include_router(friend_request_router, prefix="/friend_requests", tags=["FriendRequest"])
app.include_router(friendship_router, prefix="/friendships", tags=["Friendship"])
app.include_router(group_router, prefix="/groups", tags=["Group"])
app.include_router(group_membership_router, prefix="/group_memberships", tags=["GroupMembership"])
app.include_router(join_request_router, prefix="/join_requests", tags=["JoinRequest"])
app.include_router(like_router, prefix="/likes", tags=["Like"])
app.include_router(message_router, prefix="/messages", tags=["Message"])
app.include_router(message_service_api_router, prefix="/message_service_apis", tags=["Message_Service_API"])
app.include_router(notification_router, prefix="/notifications", tags=["Notification"])
app.include_router(notification_preference_router, prefix="/notification_preferences", tags=["NotificationPreference"])
app.include_router(operation_router, prefix="/operations", tags=["Operation"])
app.include_router(photo_router, prefix="/photos", tags=["Photo"])
app.include_router(post_router, prefix="/posts", tags=["Post"])
app.include_router(profile_router, prefix="/profiles", tags=["Profile"])
app.include_router(report_router, prefix="/reports", tags=["Report"])
app.include_router(role_router, prefix="/roles", tags=["Role"])
app.include_router(user_router)
app.include_router(saved_list_router, prefix="/saved_lists", tags=["SavedList"])
app.include_router(user_profile_router, prefix="/user_profiles", tags=["UserProfile"])
app.include_router(user_database_router, prefix="/user_databases", tags=["User_Database"])
app.include_router(verified_badge_router, prefix="/verified_badges", tags=["VerifiedBadge"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
