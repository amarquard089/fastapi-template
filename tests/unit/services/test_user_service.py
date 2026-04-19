import uuid
from unittest.mock import AsyncMock

import pytest
from app.domains.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.user_service import UserService, get_user_service


@pytest.fixture
def service_user_payload() -> dict[str, str]:
    """Provide valid payload used in user service tests."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }


@pytest.fixture
def service_user_entity(service_user_payload: dict[str, str]) -> User:
    """Provide a user entity for service operations."""
    return User.create(**service_user_payload)


@pytest.fixture
def user_repository_mock() -> AsyncMock:
    """Provide a UserRepository mock for service tests."""
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(monkeypatch: pytest.MonkeyPatch, uow_mock: AsyncMock, user_repository_mock: AsyncMock) -> UserService:
    """Provide user service with repository dependency replaced by a mock."""

    def _build_user_repository(session: AsyncMock) -> AsyncMock:
        _ = session
        return user_repository_mock

    monkeypatch.setattr("app.services.user_service.UserRepository", _build_user_repository)
    return UserService(unit_of_work=uow_mock)


@pytest.mark.asyncio
async def test_create_user_creates_and_commits(
    user_service: UserService,
    user_repository_mock: AsyncMock,
    uow_mock: AsyncMock,
) -> None:
    created_user = await user_service.create_user(first_name="John", last_name="Doe", email="john.doe@example.com")

    user_repository_mock.create.assert_called_once()
    uow_mock.commit.assert_awaited_once()
    assert created_user == user_repository_mock.create.return_value


@pytest.mark.asyncio
async def test_create_user_invalid_email_raises_value_error(user_service: UserService) -> None:
    with pytest.raises(ValueError, match="Invalid email format"):
        await user_service.create_user(first_name="John", last_name="Doe", email="invalid-email")


@pytest.mark.asyncio
async def test_get_user_returns_user(user_service: UserService, user_repository_mock: AsyncMock) -> None:
    user_id = uuid.uuid4()
    expected_user = AsyncMock()
    user_repository_mock.get_by_id.return_value = expected_user

    user = await user_service.get_user(user_id)

    assert user is expected_user
    user_repository_mock.get_by_id.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_missing_raises_value_error(user_service: UserService, user_repository_mock: AsyncMock) -> None:
    user_id = uuid.uuid4()
    user_repository_mock.get_by_id.return_value = None

    with pytest.raises(ValueError, match=f"User with ID {user_id} not found"):
        await user_service.get_user(user_id)


@pytest.mark.asyncio
async def test_update_user_applies_changes_and_commits(
    user_service: UserService,
    user_repository_mock: AsyncMock,
    uow_mock: AsyncMock,
    service_user_entity,
) -> None:
    user_id = service_user_entity.id
    user_repository_mock.get_by_id.return_value = service_user_entity

    updated_user = await user_service.update_user(
        user_id=user_id,
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
    )

    assert updated_user is service_user_entity
    assert service_user_entity.first_name == "Jane"
    assert service_user_entity.last_name == "Smith"
    assert service_user_entity.email == "jane.smith@example.com"
    uow_mock.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_deletes_and_commits(
    user_service: UserService,
    user_repository_mock: AsyncMock,
    uow_mock: AsyncMock,
    service_user_entity,
) -> None:
    user_repository_mock.get_by_id.return_value = service_user_entity

    await user_service.delete_user(service_user_entity.id)

    user_repository_mock.delete.assert_awaited_once_with(service_user_entity)
    uow_mock.commit.assert_awaited_once()


def test_get_user_service_returns_service(uow_mock: AsyncMock) -> None:
    service = get_user_service(uow_mock)

    assert isinstance(service, UserService)
