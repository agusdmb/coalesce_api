from unittest import mock

import pytest
import requests
import requests_mock
from fastapi import status
from fastapi.testclient import TestClient

from coalesce_api import models
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
    with mock.patch("coalesce_api.constants.SOURCES", sources):
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

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == models.HealthInsuranceDetails(
        deductible=1066, stop_loss=11000, oop_max=5666
    )


def test_coalesce_endpoint_timeout(client: TestClient):
    sources = ["http://api1.com", "http://api2.com", "http://api3.com"]
    with mock.patch("coalesce_api.constants.SOURCES", sources):
        with requests_mock.Mocker() as m:
            m.get(
                sources[0],
                json={"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
            )
            m.get(sources[1], exc=requests.exceptions.Timeout)
            m.get(
                sources[2],
                json={"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
            )

            response = client.get("/coalesce", params={"member_id": "1"})

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {"detail": "Source timeout"}


def test_coalesce_endpoint_fail(client: TestClient):
    sources = ["http://api1.com", "http://api2.com", "http://api3.com"]
    with mock.patch("coalesce_api.constants.SOURCES", sources):
        with requests_mock.Mocker() as m:
            m.get(
                sources[0],
                json={"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
            )
            m.get(
                sources[1],
                json={},
            )
            m.get(
                sources[2],
                json={"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
            )

            response = client.get("/coalesce", params={"member_id": "1"})

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {"detail": "Source data corrupted"}
