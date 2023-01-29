import pytest
from fastapi.testclient import TestClient

from coalesce_api.api import app


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client


def test_ping(client: TestClient):
    response = client.get("/ping")
    assert response.json() == "pong"
