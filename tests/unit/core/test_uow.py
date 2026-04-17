from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.uow import TransactionError, UnitOfWork, get_uow


@pytest.fixture
def session() -> AsyncMock:
    """Provide an isolated async session mock for UoW tests."""
    return AsyncMock(spec=AsyncSession)


@pytest.mark.asyncio
async def test_uow_commits_and_closes_on_success(session: AsyncMock) -> None:
    """UoW should commit and close when the context exits without errors."""
    async with UnitOfWork(session) as uow:
        assert not uow.is_committed

    session.commit.assert_awaited_once()
    session.rollback.assert_not_called()
    session.close.assert_awaited_once()
    assert uow.is_committed


@pytest.mark.asyncio
async def test_uow_rolls_back_and_closes_on_exception(session: AsyncMock) -> None:
    """UoW should rollback and close when an exception is raised in context."""
    with pytest.raises(ValueError, match="boom"):
        async with UnitOfWork(session):
            raise ValueError("boom")

    session.commit.assert_not_called()
    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_commit_wraps_sqlalchemy_error(session: AsyncMock) -> None:
    """Commit should rollback and raise TransactionError on SQLAlchemy failure."""
    session.commit.side_effect = SQLAlchemyError("db is unavailable")
    uow = UnitOfWork(session)

    with pytest.raises(TransactionError, match="Failed to commit transaction") as exc_info:
        await uow.commit()

    assert isinstance(exc_info.value.original_error, SQLAlchemyError)
    session.rollback.assert_awaited_once()
    assert not uow.is_committed


@pytest.mark.asyncio
async def test_operation_methods_delegate_to_session(session: AsyncMock) -> None:
    """Add/delete/refresh/rollback methods should delegate to the session."""
    uow = UnitOfWork(session)
    item = object()

    uow.add(item)
    uow.add_all([item])
    await uow.delete(item)
    await uow.refresh(item)
    await uow.rollback()

    session.add.assert_called_once_with(item)
    session.add_all.assert_called_once_with([item])
    session.delete.assert_awaited_once_with(item)
    session.refresh.assert_awaited_once_with(item)
    session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_uow_yields_unit_of_work_and_commits(session: AsyncMock) -> None:
    """Dependency generator should yield a UoW and commit on normal completion."""
    gen = get_uow(session)
    uow = await anext(gen)

    assert isinstance(uow, UnitOfWork)

    with pytest.raises(StopAsyncIteration):
        await gen.asend(None)

    session.commit.assert_awaited_once()
    session.close.assert_awaited_once()
