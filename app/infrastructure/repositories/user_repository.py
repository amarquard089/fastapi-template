"""Repository implementation for managing User entities."""

from typing import Annotated

from fastapi import Depends

from app.core.uow import UoWDep
from app.domains.user.user import User
from app.infrastructure.repositories.repository import Repository


class UserRepository(Repository[User]):
    """Repository for managing User entities."""


def get_user_repository(uow: UoWDep) -> UserRepository:
    """Dependency function to get a UserRepository instance.

    Args:
        uow (UoWDep): The unit of work dependency.

    Returns:
        UserRepository: An instance of UserRepository.

    """
    return UserRepository(uow.session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
