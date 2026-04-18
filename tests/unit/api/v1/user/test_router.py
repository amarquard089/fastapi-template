import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient


def _build_public_user_payload() -> dict[str, str]:
    user_id = uuid.uuid4()
    return {
        "id": str(user_id),
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "created_at": "2026-04-18T08:00:00Z",
        "updated_at": "2026-04-18T08:00:00Z",
    }


@pytest.mark.asyncio
async def test_get_user_success(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user = _build_public_user_payload()
    user_service_mock.get_user.return_value = user

    response = test_app.get(f"/api/v1/users/{user['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "john.doe@example.com"
    user_service_mock.get_user.assert_awaited_once_with(uuid.UUID(user["id"]))


@pytest.mark.asyncio
async def test_get_user_not_found_returns_404(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid.uuid4()
    user_service_mock.get_user.side_effect = ValueError("user not found")

    response = test_app.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}


@pytest.mark.asyncio
async def test_create_user_success(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user = _build_public_user_payload()
    user_service_mock.create_user.return_value = user

    response = test_app.post(
        "/api/v1/users/",
        params={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    user_service_mock.create_user.assert_awaited_once_with(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
    )


@pytest.mark.asyncio
async def test_create_user_validation_error_returns_400(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user_service_mock.create_user.side_effect = ValueError("Invalid email format")

    response = test_app.post(
        "/api/v1/users/",
        params={"first_name": "John", "last_name": "Doe", "email": "not-an-email"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email format"}


@pytest.mark.asyncio
async def test_update_user_success(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user = _build_public_user_payload()
    user_id = uuid.UUID(user["id"])
    user_service_mock.update_user.return_value = user

    response = test_app.put(
        f"/api/v1/users/{user_id}",
        params={"first_name": "Jane", "email": "jane.doe@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(user_id)
    user_service_mock.update_user.assert_awaited_once_with(
        user_id=user_id,
        first_name="Jane",
        last_name=None,
        email="jane.doe@example.com",
    )


@pytest.mark.asyncio
async def test_update_user_not_found_returns_404(test_app: TestClient, user_service_mock: AsyncMock) -> None:
    user_id = uuid.uuid4()
    user_service_mock.update_user.side_effect = ValueError("user not found")

    response = test_app.put(f"/api/v1/users/{user_id}", params={"first_name": "Jane"})

    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}
