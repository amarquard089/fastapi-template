import uuid
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from app.domains import Entity
from app.infrastructure.repositories.repository import Repository
from sqlmodel import Field


class MockEntity(Entity, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str


class MockEntityRepository(Repository[MockEntity]):
    """Concrete repository used to test generic repository behavior."""


@pytest.fixture
def repository(session_mock: AsyncMock) -> MockEntityRepository:
    """Provide a concrete generic repository instance."""
    return MockEntityRepository(session=session_mock)


@pytest.fixture
def mock_entity_payload() -> dict[str, str]:
    """Provide valid payload for generic repository entity fixtures."""
    return {
        "name": "mock-entity",
    }


@pytest.fixture
def mock_entity(mock_entity_payload: dict[str, Any]) -> MockEntity:
    """Provide a mock entity used in base repository tests."""
    return MockEntity(**mock_entity_payload)


def test_get_entity_type(repository, mock_entity) -> None:
    assert repository._get_entity_type() is type(mock_entity)


def test_create_adds_entity_to_session(repository, session_mock: AsyncMock, mock_entity) -> None:
    created = repository.create(mock_entity)

    assert created is mock_entity
    session_mock.add.assert_called_once_with(mock_entity)


@pytest.mark.asyncio
async def test_get_by_id_returns_first_match(repository, session_mock: AsyncMock, mock_entity) -> None:
    entity_id = uuid.uuid4()
    result = Mock()
    result.first.return_value = mock_entity
    session_mock.exec.return_value = result

    found = await repository.get_by_id(entity_id)

    assert found is mock_entity
    session_mock.exec.assert_awaited_once()
    result.first.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_returns_all_rows(repository, session_mock: AsyncMock, mock_entity) -> None:
    result = Mock()
    result.all.return_value = [mock_entity]
    session_mock.exec.return_value = result

    found = await repository.get_all()

    assert list(found) == [mock_entity]
    session_mock.exec.assert_awaited_once()
    result.all.assert_called_once()


@pytest.mark.asyncio
async def test_delete_delegates_to_session(repository, session_mock: AsyncMock, mock_entity) -> None:
    await repository.delete(mock_entity)

    session_mock.delete.assert_awaited_once_with(mock_entity)
