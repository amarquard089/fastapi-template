"""User domain entity definition."""

import re

from app.domains.entity import Entity, TimestampMixin
from app.domains.user.base import UserBase
from app.domains.user.exceptions import (
    EmptyEmailException,
    EmptyNameException,
    InvalidEmailException,
    InvalidNameException,
)


class User(UserBase, Entity, TimestampMixin, table=True):
    """User entity representing a user in the system."""

    @classmethod
    def create(cls, first_name: str, last_name: str, email: str) -> "User":
        """Create a new User instance with validation.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.

        Returns:
            User: A new User instance.

        Raises:
            EmptyNameException: If the first name or last name is empty.
            EmptyEmailException: If the email is empty.
            InvalidEmailException: If the email format is invalid.
            InvalidNameException: If the first name or last name format is invalid.

        """
        if not first_name:
            raise EmptyNameException("First name cannot be empty")
        if not cls._valid_name(first_name):
            raise InvalidNameException("Invalid first name format")
        if not last_name:
            raise EmptyNameException("Last name cannot be empty")
        if not cls._valid_name(last_name):
            raise InvalidNameException("Invalid last name format")
        if not email:
            raise EmptyEmailException("Email cannot be empty")
        if not cls._valid_email(email):
            raise InvalidEmailException("Invalid email format")
        return cls(first_name=first_name, last_name=last_name, email=email)

    def change_first_name(self, new_first_name: str) -> None:
        """Change the user's first name."""
        if not new_first_name:
            raise EmptyNameException("First name cannot be empty")
        if not self._valid_name(new_first_name):
            raise InvalidNameException("Invalid first name format")
        self.first_name = new_first_name
        self.updated_at = self._current_time()

    def change_last_name(self, new_last_name: str) -> None:
        """Change the user's last name."""
        if not new_last_name:
            raise EmptyNameException("Last name cannot be empty")
        if not self._valid_name(new_last_name):
            raise InvalidNameException("Invalid last name format")
        self.last_name = new_last_name
        self.updated_at = self._current_time()

    def change_email(self, new_email: str) -> None:
        """Change the user's email."""
        if not new_email:
            raise EmptyEmailException("Email cannot be empty")
        if not self._valid_email(new_email):
            raise InvalidEmailException("Invalid email format")
        self.email = new_email
        self.updated_at = self._current_time()

    @staticmethod
    def _valid_name(name: str) -> bool:
        """Validate the name.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.

        """
        return len(name) > 0

    @staticmethod
    def _valid_email(email: str) -> bool:
        """Validate the email format.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.

        """
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(email_regex, email) is not None
