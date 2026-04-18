"""Data Transfer Objects (DTOs) for public-facing representations of domain entities."""

import uuid

from sqlmodel import SQLModel


class PublicEntity(SQLModel):
    """Base class for entities that can be exposed publicly, without sensitive information."""

    id: uuid.UUID


class PublicTimestampMixin(SQLModel):
    """Mixin to add created_at and updated_at timestamps to public entities."""

    created_at: str
    updated_at: str


class PublicUserAuditMixin(PublicTimestampMixin):
    """Mixin to add created_by and updated_by user tracking to public entities."""

    created_by: uuid.UUID
    updated_by: uuid.UUID


class PublicSoftDeleteMixin(SQLModel):
    """Mixin to add soft delete information to public entities."""

    deleted_at: str | None
    deleted_by: uuid.UUID | None
    is_deleted: bool
