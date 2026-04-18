from typing import Generator
from unittest.mock import AsyncMock

import pytest
from app.main import app
from app.services.user_service import UserService, get_user_service


@pytest.fixture
def dummy_user_id() -> str:
    """Fixture for a dummy user ID."""
    return "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture
def dummy_user(dummy_user_id: str) -> dict[str, str]:
    """Helper function to create a dummy user payload."""
    return {
        "id": dummy_user_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "created_at": "2026-04-18T08:00:00Z",
        "updated_at": "2026-04-18T08:00:00Z",
    }


@pytest.fixture
def user_service_mock(dummy_user: dict[str, str]) -> Generator[AsyncMock, None, None]:
    """Override the router dependency with an async mock service."""
    mock = AsyncMock(spec=UserService)
    mock.get_user.return_value = dummy_user

    def override_user_service() -> AsyncMock:
        return mock

    app.dependency_overrides[get_user_service] = override_user_service
    yield mock
    app.dependency_overrides.pop(get_user_service, None)
