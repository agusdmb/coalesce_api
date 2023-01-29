import requests_mock

from coalesce_api import __version__, coalesce_api


def test_version():
    assert __version__ == "0.1.0"


def test_get_health_insurance_details_1():
    url = "http://api1.com"
    member_id = "1"
    with requests_mock.Mocker() as m:
        m.get(
            url,
            json={"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
        )
        health_insurance_deatails = coalesce_api.get_health_insurance_details(
            url, member_id
        )
        assert health_insurance_deatails == coalesce_api.HealthInsuranceDetails(
            deductible=1000, stop_loss=10000, oop_max=5000
        )


def test_get_health_insurance_details_2():
    url = "http://api2.com"
    member_id = "2"
    with requests_mock.Mocker() as m:
        m.get(
            url,
            json={"deductible": 1200, "stop_loss": 13000, "oop_max": 6000},
        )
        health_insurance_deatails = coalesce_api.get_health_insurance_details(
            url, member_id
        )
        assert health_insurance_deatails == coalesce_api.HealthInsuranceDetails(
            deductible=1200, stop_loss=13000, oop_max=6000
        )
