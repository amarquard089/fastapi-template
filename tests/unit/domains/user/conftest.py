import pytest
from app.domains.user.user import User


@pytest.fixture
def user_payload() -> dict[str, str]:
    """Provide valid user creation payload used by domain/service tests."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }


@pytest.fixture
def user_entity(user_payload: dict[str, str]) -> User:
    """Provide a valid user entity instance."""
    return User.create(**user_payload)
