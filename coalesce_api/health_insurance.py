import requests
from pydantic import BaseModel

TIMEOUT_SECONDS = 5.0


class HealthInsuranceDetails(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int


def get_health_insurance_details(url: str, member_id: str) -> HealthInsuranceDetails:
    response = requests.get(
        url, params={"member_id": member_id}, timeout=TIMEOUT_SECONDS
    )
    health_insurance_details = HealthInsuranceDetails(**response.json())
    return health_insurance_details
