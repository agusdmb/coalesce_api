from typing import Sequence

import requests
from pydantic import BaseModel, ValidationError

TIMEOUT_SECONDS = 5.0


class HealthInsuranceDetails(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int


class HealthInsuranceException(Exception):
    pass


class HealthInsuranceAPITimeout(HealthInsuranceException):
    pass


class HealthInsuranceValueError(HealthInsuranceException):
    pass


class HealthInsuranceAPIValidationError(HealthInsuranceException):
    pass


def get_health_insurance_details(url: str, member_id: str) -> HealthInsuranceDetails:
    try:
        response = requests.get(
            url, params={"member_id": member_id}, timeout=TIMEOUT_SECONDS
        )
    except requests.exceptions.Timeout as e:
        raise HealthInsuranceAPITimeout() from e
    try:
        health_insurance_details = HealthInsuranceDetails(**response.json())
    except ValidationError as e:
        raise HealthInsuranceAPIValidationError() from e
    return health_insurance_details


def average_health_insurances(
    health_insurances: Sequence[HealthInsuranceDetails],
) -> HealthInsuranceDetails:
    if not health_insurances:
        raise HealthInsuranceValueError(
            "Must provide at least one Health Insurance to compute average."
        )

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


def get_coalesce_health_insurance(
    sources: list[str], member_id: str
) -> HealthInsuranceDetails:
    return average_health_insurances(
        [get_health_insurance_details(source, member_id) for source in sources]
    )
