import pytest
import requests
import requests_mock
from hypothesis import example, given
from hypothesis import strategies as st

from coalesce_api import __version__, exceptions, health_insurance, models, strategies


def test_version():
    assert __version__ == "0.1.0"


url_strategy = st.from_regex(
    r"https?://[a-zA-Z0-9]+\.[a-zA-Z]+\.(com|org)", fullmatch=True
)


@example(
    url="http://api1.com", member_id="1", deductible=1000, stop_loss=10000, oop_max=5000
)
@example(
    url="http://api2.com", member_id="2", deductible=1200, stop_loss=13000, oop_max=6000
)
@example(
    url="http://api3.com", member_id="1", deductible=1000, stop_loss=10000, oop_max=6000
)
@given(url_strategy, st.integers(), st.integers(), st.integers(), st.integers())
def test_get_health_insurance_details(url, member_id, deductible, stop_loss, oop_max):
    with requests_mock.Mocker() as m:
        m.get(
            url,
            json={"deductible": deductible, "stop_loss": stop_loss, "oop_max": oop_max},
        )
        health_insurance_deatails = health_insurance.get_health_insurance_details(
            url, member_id
        )
        assert health_insurance_deatails == models.HealthInsuranceDetails(
            deductible=deductible, stop_loss=stop_loss, oop_max=oop_max
        )


def test_get_health_insurance_details_fails():
    url = "http://api1.com"
    member_id = "1"

    with requests_mock.Mocker() as m:
        m.get(url, exc=requests.exceptions.Timeout)
        with pytest.raises(exceptions.HealthInsuranceAPITimeout):
            health_insurance.get_health_insurance_details(url, member_id)


def test_get_health_insurance_details_bad_data():
    url = "http://api1.com"
    member_id = "1"

    with requests_mock.Mocker() as m:
        m.get(
            url,
            json={},
        )
        with pytest.raises(exceptions.HealthInsuranceAPIValidationError):
            health_insurance.get_health_insurance_details(url, member_id)


@pytest.mark.parametrize(
    "health_insurances,avg_health_insurance",
    [
        (
            [models.HealthInsuranceDetails(deductible=0, stop_loss=0, oop_max=0)],
            models.HealthInsuranceDetails(deductible=0, stop_loss=0, oop_max=0),
        ),
        (
            [
                models.HealthInsuranceDetails(
                    deductible=1000, stop_loss=10000, oop_max=5000
                ),
                models.HealthInsuranceDetails(
                    deductible=1200, stop_loss=13000, oop_max=6000
                ),
                models.HealthInsuranceDetails(
                    deductible=1000, stop_loss=10000, oop_max=6000
                ),
            ],
            models.HealthInsuranceDetails(
                deductible=1066, stop_loss=11000, oop_max=5666
            ),
        ),
    ],
)
def test_average_health_insurances(health_insurances, avg_health_insurance):
    assert avg_health_insurance == strategies.average_health_insurances(
        health_insurances
    )


def test_average_health_insurances_empty_case():
    with pytest.raises(exceptions.HealthInsuranceValueError):
        strategies.average_health_insurances([])


def test_get_coalesce_health_insurance():
    member_id = "1"
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
        coalesce_health_insurance = health_insurance.get_coalesce_health_insurance(
            sources, member_id
        )

    assert coalesce_health_insurance == models.HealthInsuranceDetails(
        deductible=1066, stop_loss=11000, oop_max=5666
    )
