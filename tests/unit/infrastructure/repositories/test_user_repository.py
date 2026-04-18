from unittest.mock import AsyncMock, Mock

from app.domains.user.user import User
from app.infrastructure.repositories.user_repository import UserRepository, get_user_repository


def test_user_repository_entity_type(session_mock: AsyncMock) -> None:
    user_repository = UserRepository(session=session_mock)

    assert user_repository._get_entity_type() is User


def test_get_user_repository_returns_repository_with_uow_session() -> None:
    uow_mock = Mock()
    uow_mock.session = AsyncMock()

    repository = get_user_repository(uow_mock)

    assert isinstance(repository, UserRepository)
    assert repository.session is uow_mock.session
