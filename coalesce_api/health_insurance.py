from typing import Sequence

import requests
from pydantic import BaseModel

TIMEOUT_SECONDS = 5.0


class HealthInsuranceDetails(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int


class HealthInsuranceException(Exception):
    pass


class HealthInsuranceAPITimeout(HealthInsuranceException):
    pass


def get_health_insurance_details(url: str, member_id: str) -> HealthInsuranceDetails:
    try:
        response = requests.get(
            url, params={"member_id": member_id}, timeout=TIMEOUT_SECONDS
        )
    except requests.exceptions.Timeout as e:
        raise HealthInsuranceAPITimeout() from e
    health_insurance_details = HealthInsuranceDetails(**response.json())
    return health_insurance_details


def average_health_insurances(
    health_insurances: Sequence[HealthInsuranceDetails],
) -> HealthInsuranceDetails:
    deductible_avg = 0
    stop_loss_avg = 0
    oop_max_avg = 0
    for health_insurance in health_insurances:
        deductible_avg += health_insurance.deductible
        stop_loss_avg += health_insurance.stop_loss
        oop_max_avg += health_insurance.oop_max
    return HealthInsuranceDetails(
        deductible=deductible_avg // len(health_insurances),
        stop_loss=stop_loss_avg // len(health_insurances),
        oop_max=oop_max_avg // len(health_insurances),
    )
