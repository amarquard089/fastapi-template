import pytest
from app.domains.user.exceptions import (
    EmptyEmailException,
    EmptyNameException,
    InvalidEmailException,
    InvalidNameException,
)
from app.domains.user.user import User


def test_create_user_success(user_payload: dict[str, str]) -> None:
    user = User.create(**user_payload)

    assert user.first_name == user_payload["first_name"]
    assert user.last_name == user_payload["last_name"]
    assert user.email == user_payload["email"]


def test_create_user_empty_first_name_raises(user_payload: dict[str, str]) -> None:
    payload = {**user_payload, "first_name": ""}

    with pytest.raises(EmptyNameException, match="First name cannot be empty"):
        User.create(**payload)


def test_create_user_empty_last_name_raises(user_payload: dict[str, str]) -> None:
    payload = {**user_payload, "last_name": ""}

    with pytest.raises(EmptyNameException, match="Last name cannot be empty"):
        User.create(**payload)


def test_create_user_empty_email_raises(user_payload: dict[str, str]) -> None:
    payload = {**user_payload, "email": ""}

    with pytest.raises(EmptyEmailException, match="Email cannot be empty"):
        User.create(**payload)


def test_create_user_invalid_email_raises(user_payload: dict[str, str]) -> None:
    payload = {**user_payload, "email": "invalid-email"}

    with pytest.raises(InvalidEmailException, match="Invalid email format"):
        User.create(**payload)


def test_create_user_invalid_first_name_raises(user_payload: dict[str, str], monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {**user_payload, "first_name": "John"}
    monkeypatch.setattr(User, "_valid_name", staticmethod(lambda _: False))

    with pytest.raises(InvalidNameException, match="Invalid first name format"):
        User.create(**payload)


def test_create_user_invalid_last_name_raises(user_payload: dict[str, str], monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {**user_payload, "last_name": "Doe"}

    call_count = {"count": 0}

    def fake_valid_name(_: str) -> bool:
        call_count["count"] += 1
        return call_count["count"] == 1

    monkeypatch.setattr(User, "_valid_name", staticmethod(fake_valid_name))

    with pytest.raises(InvalidNameException, match="Invalid last name format"):
        User.create(**payload)


def test_change_methods_update_values(user_entity: User) -> None:
    user_entity.change_first_name("Jane")
    user_entity.change_last_name("Smith")
    user_entity.change_email("jane.smith@example.com")

    assert user_entity.first_name == "Jane"
    assert user_entity.last_name == "Smith"
    assert user_entity.email == "jane.smith@example.com"


def test_change_first_name_empty_raises(user_entity: User) -> None:
    with pytest.raises(EmptyNameException, match="First name cannot be empty"):
        user_entity.change_first_name("")


def test_change_first_name_invalid_raises(user_entity: User, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(User, "_valid_name", staticmethod(lambda _: False))

    with pytest.raises(InvalidNameException, match="Invalid first name format"):
        user_entity.change_first_name("Invalid")


def test_change_last_name_empty_raises(user_entity: User) -> None:
    with pytest.raises(EmptyNameException, match="Last name cannot be empty"):
        user_entity.change_last_name("")


def test_change_last_name_invalid_raises(user_entity: User, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(User, "_valid_name", staticmethod(lambda _: False))

    with pytest.raises(InvalidNameException, match="Invalid last name format"):
        user_entity.change_last_name("Invalid")


def test_change_email_empty_raises(user_entity: User) -> None:
    with pytest.raises(EmptyEmailException, match="Email cannot be empty"):
        user_entity.change_email("")


def test_change_email_invalid_raises(user_entity: User) -> None:
    with pytest.raises(InvalidEmailException, match="Invalid email format"):
        user_entity.change_email("invalid-email")
