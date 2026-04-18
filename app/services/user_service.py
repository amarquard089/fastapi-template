"""Service layer for user-related business logic."""

import uuid
from typing import Annotated

from fastapi import Depends

from app.core.uow import UnitOfWork, UoWDep
from app.domains.user.exceptions import (
    EmptyEmailException,
    EmptyNameException,
    InvalidEmailException,
    InvalidNameException,
)
from app.domains.user.user import User
from app.infrastructure.repositories.user_repository import UserRepository


class UserService:
    """Service layer for user-related business logic."""

    def __init__(self, unit_of_work: UnitOfWork):
        """Initialize the UserService with a UnitOfWork.

        Args:
            unit_of_work (UnitOfWork): The unit of work instance.

        """
        self.uow = unit_of_work
        self.user_repository = UserRepository(self.uow.session)

    async def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
    ) -> User:
        """Create a new user with the given first name, last name, and email.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the user creation fails due to validation errors.

        """
        try:
            new_user = User.create(first_name=first_name, last_name=last_name, email=email)
        except (EmptyNameException, EmptyEmailException, InvalidNameException, InvalidEmailException) as e:
            raise ValueError(str(e)) from e
        async with self.uow:
            user = self.user_repository.create(new_user)
            await self.uow.commit()
        return user

    async def get_user(self, user_id: uuid.UUID) -> User:
        """Retrieve a user by their ID.

        Args:
            user_id (uuid.UUID): The ID of the user to retrieve.

        Returns:
            User: The retrieved user instance.

        Raises:
            ValueError: If the user with the given ID is not found.

        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    async def update_user(
        self, user_id: uuid.UUID, first_name: str | None = None, last_name: str | None = None, email: str | None = None
    ) -> User:
        """Update an existing user's information.

        Args:
            user_id (uuid.UUID): The ID of the user to update.
            first_name (str | None): The new first name of the user (optional).
            last_name (str | None): The new last name of the user (optional).
            email (str | None): The new email address of the user (optional).

        Returns:
            User: The updated user instance.

        Raises:
            ValueError: If the user with the given ID is not found.

        """
        user = await self.get_user(user_id)
        async with self.uow:
            if first_name:
                user.change_first_name(first_name)
            if last_name:
                user.change_last_name(last_name)
            if email:
                user.change_email(email)
            await self.uow.commit()
        return user

    async def delete_user(self, user_id: uuid.UUID) -> None:
        """Delete a user by their ID.

        Args:
            user_id (uuid.UUID): The ID of the user to delete.

        Raises:
            ValueError: If the user with the given ID is not found.

        """
        user = await self.get_user(user_id)
        async with self.uow:
            await self.user_repository.delete(user)
            await self.uow.commit()


def get_user_service(uow: UoWDep) -> UserService:
    """Dependency function to get a UserService instance.

    Args:
        uow (UoWDep): The unit of work dependency.

    Returns:
        UserService: An instance of UserService.

    """
    return UserService(unit_of_work=uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
