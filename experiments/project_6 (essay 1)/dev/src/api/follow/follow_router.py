from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.follow.follow_dto import FollowRequest, FollowResponse, UnfollowRequest
from src.orm.follow.follow_orm import FollowORM

"""
Api layer for the Follow domain class

Package: api.follow
Layer: api
Related tasks: #164
Requirement coverage:
- User Follow/Unfollow Functionality
"""

router = APIRouter()


def _follower_count(db: Session, target_profile_id: str) -> int:
    return (
        db.query(FollowORM)
        .filter(FollowORM.followingId == target_profile_id, FollowORM.state == "active")
        .count()
    )


@router.post("/follow", response_model=FollowResponse)
def follow_user(data: FollowRequest, db: Session = Depends(get_db)) -> FollowResponse:
    existing = (
        db.query(FollowORM)
        .filter(
            FollowORM.followerId == data.initiatorId,
            FollowORM.followingId == data.targetProfileId,
        )
        .first()
    )
    if existing is None:
        db.add(FollowORM(followerId=data.initiatorId, followingId=data.targetProfileId, state="active"))
        db.commit()
    elif existing.state != "active":
        existing.state = "active"
        db.commit()

    return FollowResponse(
        success=True,
        newFollowerCount=_follower_count(db, data.targetProfileId),
        message="Followed successfully",
    )


@router.post("/unfollow", response_model=FollowResponse)
def unfollow_user(data: UnfollowRequest, db: Session = Depends(get_db)) -> FollowResponse:
    existing = (
        db.query(FollowORM)
        .filter(
            FollowORM.followerId == data.initiatorId,
            FollowORM.followingId == data.targetProfileId,
        )
        .first()
    )
    if existing is not None and existing.state == "active":
        existing.state = "inactive"
        db.commit()

    return FollowResponse(
        success=True,
        newFollowerCount=_follower_count(db, data.targetProfileId),
        message="Unfollowed successfully",
    )
