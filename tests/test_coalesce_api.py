from coalesce_api import __version__, coalesce_api


def test_version():
    assert __version__ == "0.1.0"


def test_get_health_insurance_details():
    url = "test_url"
    member_id = "member_id"
    health_insurance_deatails = coalesce_api.get_health_insurance_details(
        url, member_id
    )
    assert health_insurance_deatails == coalesce_api.HealthInsuranceDetails(
        deductible=1000, stop_loss=10000, oop_max=5000
    )
