"""Custom domain exceptions for user domain logic."""


class EmptyNameException(Exception):
    """Custom exception raised when an empty name is provided."""

    pass


class InvalidNameException(Exception):
    """Custom exception raised when an invalid name is provided."""

    pass


class EmptyEmailException(Exception):
    """Custom exception raised when an empty email is provided."""

    pass


class InvalidEmailException(Exception):
    """Custom exception raised when an invalid email is provided."""

    pass
