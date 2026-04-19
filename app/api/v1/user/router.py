"""API router for user-related endpoints."""

import uuid

from fastapi import APIRouter, HTTPException

from app.api.v1.user.schemas import CreateUserRequest, PublicUser, UpdateUserRequest
from app.services.user_service import UserServiceDep

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/{user_id}", response_model=PublicUser)
async def get_user(user_id: uuid.UUID, user_service: UserServiceDep):
    """Endpoint to retrieve a user by their ID."""
    try:
        user = await user_service.get_user(user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@user_router.post("/", response_model=PublicUser)
async def create_user(new_user: CreateUserRequest, user_service: UserServiceDep):
    """Endpoint to create a new user."""
    try:
        user = await user_service.create_user(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.put("/{user_id}", response_model=PublicUser)
async def update_user(
    user_id: uuid.UUID,
    update_user: UpdateUserRequest,
    *,
    user_service: UserServiceDep,
):
    """Endpoint to update an existing user's information."""
    try:
        user = await user_service.update_user(
            user_id=user_id, first_name=update_user.first_name, last_name=update_user.last_name, email=update_user.email
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
