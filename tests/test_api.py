import pytest
import requests_mock
from fastapi.testclient import TestClient

from coalesce_api import health_insurance
from coalesce_api.api import app


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client


def test_ping(client: TestClient):
    response = client.get("/ping")
    assert response.json() == "pong"


def test_coalesce_endpoint(client: TestClient):
    sources = ["http://api1.com", "http://api2.com", "http://api3.com"]
    with requests_mock.Mocker() as m:
        m.get(
            sources[0],
            json={"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
        )
        m.get(
            sources[1],
            json={"deductible": 1200, "stop_loss": 13000, "oop_max": 6000},
        )
        m.get(
            sources[2],
            json={"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
        )

        response = client.get("/coalesce", params={"member_id": "1"})

    assert response.status_code == 200

    assert response.json() == health_insurance.HealthInsuranceDetails(
        deductible=1066, stop_loss=11000, oop_max=5666
    )
