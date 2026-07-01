from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.group_membership.group_membership_dto import GroupMembershipCreate, GroupMembershipUpdate, GroupMembershipResponse
from src.infra.group_membership.group_membership_repo_impl import SQLAlchemyGroupMembershipRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyGroupMembershipRepository:
    return SQLAlchemyGroupMembershipRepository(db)


@router.get("", response_model=list[GroupMembershipResponse])
def list_group_memberships(skip: int = 0, limit: int = 100, repo: SQLAlchemyGroupMembershipRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=GroupMembershipResponse)
def get_group_membership(item_id: int, repo: SQLAlchemyGroupMembershipRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GroupMembership not found")
    return item


@router.post("", response_model=GroupMembershipResponse, status_code=status.HTTP_201_CREATED)
def create_group_membership(data: GroupMembershipCreate, repo: SQLAlchemyGroupMembershipRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=GroupMembershipResponse)
def update_group_membership(item_id: int, data: GroupMembershipUpdate, repo: SQLAlchemyGroupMembershipRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GroupMembership not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_membership(item_id: int, repo: SQLAlchemyGroupMembershipRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GroupMembership not found")
