"""Domain entities representing core business objects."""

import datetime
import uuid

from sqlmodel import Field, SQLModel


class Entity(SQLModel):
    """Base class for all domain entities, providing common attributes and methods."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampMixin(SQLModel):
    """Mixin to add created_at and updated_at timestamps to entities."""

    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))


class UserAuditMixin(TimestampMixin):
    """Mixin to add created_by and updated_by user tracking to entities."""

    created_by: uuid.UUID = Field(index=True)
    updated_by: uuid.UUID = Field(index=True)


class SoftDeleteMixin(SQLModel):
    """Mixin to add soft delete functionality to entities."""

    deleted_at: datetime.datetime | None = Field(default=None)
    deleted_by: uuid.UUID | None = Field(default=None)
    is_deleted: bool = Field(default=False)
