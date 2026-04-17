import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_health(test_app: TestClient):
    response = test_app.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_options(test_app: TestClient):
    response = test_app.options("/health")
    assert response.status_code == 204
