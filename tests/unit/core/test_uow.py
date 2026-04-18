from unittest.mock import AsyncMock

import pytest
from app.core.uow import TransactionError, UnitOfWork, get_uow
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.asyncio
async def test_uow_commits_and_closes_on_success(session_mock: AsyncMock) -> None:
    """UoW should commit and close when the context exits without errors."""
    async with UnitOfWork(session_mock) as uow:
        assert not uow.is_committed

    session_mock.commit.assert_awaited_once()
    session_mock.rollback.assert_not_called()
    session_mock.close.assert_awaited_once()
    assert uow.is_committed


@pytest.mark.asyncio
async def test_uow_rolls_back_and_closes_on_exception(session_mock: AsyncMock) -> None:
    """UoW should rollback and close when an exception is raised in context."""
    with pytest.raises(ValueError, match="boom"):
        async with UnitOfWork(session_mock):
            raise ValueError("boom")

    session_mock.commit.assert_not_called()
    session_mock.rollback.assert_awaited_once()
    session_mock.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_commit_wraps_sqlalchemy_error(session_mock: AsyncMock) -> None:
    """Commit should rollback and raise TransactionError on SQLAlchemy failure."""
    session_mock.commit.side_effect = SQLAlchemyError("db is unavailable")
    uow = UnitOfWork(session_mock)

    with pytest.raises(TransactionError, match="Failed to commit transaction") as exc_info:
        await uow.commit()

    assert isinstance(exc_info.value.original_error, SQLAlchemyError)
    session_mock.rollback.assert_awaited_once()
    assert not uow.is_committed


@pytest.mark.asyncio
async def test_operation_methods_delegate_to_session(session_mock: AsyncMock) -> None:
    """Add/delete/refresh/rollback methods should delegate to the session."""
    uow = UnitOfWork(session_mock)
    item = object()

    uow.add(item)
    uow.add_all([item])
    await uow.delete(item)
    await uow.refresh(item)
    await uow.rollback()

    session_mock.add.assert_called_once_with(item)
    session_mock.add_all.assert_called_once_with([item])
    session_mock.delete.assert_awaited_once_with(item)
    session_mock.refresh.assert_awaited_once_with(item)
    session_mock.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_uow_yields_unit_of_work_and_commits(session_mock: AsyncMock) -> None:
    """Dependency generator should yield a UoW and commit on normal completion."""
    gen = get_uow(session_mock)
    uow = await anext(gen)

    assert isinstance(uow, UnitOfWork)

    with pytest.raises(StopAsyncIteration):
        await gen.asend(None)

    session_mock.commit.assert_awaited_once()
    session_mock.close.assert_awaited_once()
