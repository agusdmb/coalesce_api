import pytest
import requests
import requests_mock
from hypothesis import example, given
from hypothesis import strategies as st

from coalesce_api import __version__, health_insurance


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
        assert health_insurance_deatails == health_insurance.HealthInsuranceDetails(
            deductible=deductible, stop_loss=stop_loss, oop_max=oop_max
        )


def test_get_health_insurance_details_fails():
    url = "http://api1.com"
    member_id = "1"

    with requests_mock.Mocker() as m:
        m.get(url, exc=requests.exceptions.Timeout)
        with pytest.raises(health_insurance.HealthInsuranceAPITimeout):
            health_insurance.get_health_insurance_details(url, member_id)


@pytest.mark.parametrize(
    "health_insurances,avg_health_insurance",
    [
        (
            [
                health_insurance.HealthInsuranceDetails(
                    deductible=0, stop_loss=0, oop_max=0
                )
            ],
            health_insurance.HealthInsuranceDetails(
                deductible=0, stop_loss=0, oop_max=0
            ),
        ),
    ],
)
def test_average_health_insurances(health_insurances, avg_health_insurance):
    assert avg_health_insurance == health_insurance.average_health_insurances(
        health_insurances
    )
