from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse, UserListResponse
from src.service.user.user_service import UserService

router = APIRouter()


def _service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("", response_model=UserListResponse)
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(_service),
):
    return service.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    service: UserService = Depends(_service),
):
    item = service.get_user(user_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return item


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreateRequest,
    service: UserService = Depends(_service),
):
    try:
        return service.create_user(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    data: UserUpdateRequest,
    service: UserService = Depends(_service),
):
    try:
        item = service.update_user(user_id, data)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    service: UserService = Depends(_service),
):
    if not service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.post("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(
    user_id: str,
    service: UserService = Depends(_service),
):
    item = service.deactivate_user(user_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return item


@router.post("/{user_id}/activate", response_model=UserResponse)
def activate_user(
    user_id: str,
    service: UserService = Depends(_service),
):
    item = service.activate_user(user_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return item
