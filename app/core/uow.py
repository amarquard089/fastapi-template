"""Unit of Work implementation for managing database transactions."""

from collections.abc import AsyncGenerator
from types import TracebackType
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import SessionDep


class TransactionError(Exception):
    """Raised when a transaction fails to commit."""

    def __init__(self, original_error: Exception, message: str = "Transaction failed"):
        """Initialize transaction error with original database exception."""
        self.original_error = original_error
        super().__init__(message)


class UnitOfWork:
    """Manage transactional work against an async database session."""

    def __init__(self, session: AsyncSession):
        """Initialize the unit of work with a database session."""
        self.session = session
        self._committed = False

    async def __aenter__(self) -> "UnitOfWork":
        """Enter the async context and return the current unit of work."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Commit on success, rollback on errors, and always close the session."""
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        """Explicitly commit the transaction."""
        try:
            await self.session.commit()
            self._committed = True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise TransactionError(e, f"Failed to commit transaction: {e!s}") from e

    def add(self, instance: object) -> None:
        """Add an instance to the current transaction."""
        self.session.add(instance)

    def add_all(self, instances: list[object]) -> None:
        """Add multiple instances to the current transaction."""
        self.session.add_all(instances)

    async def delete(self, instance: object) -> None:
        """Delete an instance in the current transaction."""
        await self.session.delete(instance)

    async def refresh(self, instance: object) -> None:
        """Refresh an instance with the latest data from the database."""
        await self.session.refresh(instance)

    async def rollback(self) -> None:
        """Explicitly rollback the transaction."""
        await self.session.rollback()

    @property
    def is_committed(self) -> bool:
        """Check if the transaction was successfully committed."""
        return self._committed


# @asynccontextmanager
# async def get_uow(session: AsyncSession) -> AsyncGenerator[UnitOfWork, None]:
#     async with UnitOfWork(session) as uow:
#         yield uow


async def get_uow(
    session: SessionDep,
) -> AsyncGenerator[UnitOfWork, None]:
    """Provide a managed unit of work bound to the request session."""
    async with UnitOfWork(session) as uow:
        yield uow


UoWDep = Annotated[UnitOfWork, Depends(get_uow)]
