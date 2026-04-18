from typing import Generator
from unittest.mock import AsyncMock

import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def session_mock() -> AsyncMock:
    """Provide an async database session mock for repository tests."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def db_session(session_mock: AsyncMock) -> Generator[AsyncMock, None, None]:
    """Fixture for mocking the database session.

    Reference: https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency"""
    from app.core.db import get_engine

    mock_session = session_mock

    async def override():
        yield mock_session

    app.dependency_overrides[get_engine] = override
    yield mock_session
    app.dependency_overrides.clear()


@pytest.fixture
def test_app(db_session: AsyncMock) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
