"""Generic repository implementation for managing domain entities."""

import uuid
from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.entity import Entity


class Repository[T: Entity]:
    """Generic repository for managing entities."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session (AsyncSession): The asynchronous database session.

        """
        self.session = session

    def _get_entity_type(self) -> type[T]:
        """Get the entity type managed by this repository.

        Returns:
            type[T]: The type of the entity managed by this repository.

        """
        return self.__class__.__orig_bases__[0].__args__[0]  # type: ignore

    def create(self, entity: T) -> T:
        """Create a new entity in the repository.

        Args:
            entity (T): The entity to create.

        Returns:
            T: The created entity.

        """
        self.session.add(entity)
        return entity

    async def get_by_id(self, entity_id: uuid.UUID) -> T | None:
        """Get an entity by its ID.

        Args:
            entity_id (uuid.UUID): The ID of the entity.

        Returns:
            T | None: The entity if found, otherwise None.

        """
        result = await self.session.exec(select(self._get_entity_type()).where(self._get_entity_type().id == entity_id))
        return result.first()

    async def get_all(self) -> Sequence[T]:
        """Get all entities.

        Returns:
            Sequence[T]: A sequence of all entities.

        """
        result = await self.session.exec(select(self._get_entity_type()))
        return result.all()

    async def delete(self, entity: T) -> None:
        """Delete an entity from the repository.

        Args:
            entity (T): The entity to delete.

        """
        await self.session.delete(entity)
