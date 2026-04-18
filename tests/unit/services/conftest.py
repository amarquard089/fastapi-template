from unittest.mock import AsyncMock

import pytest
from app.core.uow import UnitOfWork


@pytest.fixture
def uow_mock(session_mock: AsyncMock) -> AsyncMock:
    """Provide a UnitOfWork mock configured for async context manager usage."""
    mock = AsyncMock(spec=UnitOfWork)
    mock.session = session_mock
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    return mock
