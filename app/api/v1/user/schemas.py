"""Schemas for user-related API endpoints."""

from app.api.public_schemas import PublicEntity, PublicTimestampMixin
from app.domains.user import UserBase


class PublicUser(UserBase, PublicEntity, PublicTimestampMixin):
    """Public representation of a user for API responses."""
