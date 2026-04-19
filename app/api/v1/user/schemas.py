"""Schemas for user-related API endpoints."""

from pydantic import BaseModel

from app.api.public_schemas import PublicEntity, PublicTimestampMixin
from app.domains.user import UserBase


class PublicUser(UserBase, PublicEntity, PublicTimestampMixin):
    """Public representation of a user for API responses."""


class CreateUserRequest(UserBase):
    """Schema for creating a new user via API requests."""


class UpdateUserRequest(BaseModel):
    """Schema for updating an existing user via API requests."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
