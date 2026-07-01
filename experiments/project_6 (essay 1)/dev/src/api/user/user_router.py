from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.config.dependencies import Container
from src.dto.user.user_dto import RegistrationRequest, RegistrationResponse, LoginRequest, LoginResponse, UserCreate, UserUpdate, UserResponse
from src.service.user.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegistrationRequest, service: UserService = Depends(Container.get_user_service)) -> RegistrationResponse:
    try:
        return service.register(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, service: UserService = Depends(Container.get_user_service)) -> LoginResponse:
    try:
        return service.login(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, service: UserService = Depends(Container.get_user_service)) -> list[UserResponse]:
    return service.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=Optional[UserResponse])
def get_user(user_id: int, service: UserService = Depends(Container.get_user_service)) -> Optional[UserResponse]:
    user = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=Optional[UserResponse])
def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(Container.get_user_service)) -> Optional[UserResponse]:
    user = service.update(user_id, data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(Container.get_user_service)) -> None:
    deleted = service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
