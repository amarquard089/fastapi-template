from typing import Generator
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession
from src.main import app


@pytest.fixture
def db_session() -> Generator[AsyncMock, None, None]:
    """Fixture for mocking the database session.

    Reference: https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency"""
    from src.core.db import get_engine

    mock_session = AsyncMock(spec=AsyncSession)

    async def override():
        yield mock_session

    app.dependency_overrides[get_engine] = override
    yield mock_session
    app.dependency_overrides.clear()


@pytest.fixture
def test_app(db_session: AsyncMock) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
