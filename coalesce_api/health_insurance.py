import requests
from pydantic import ValidationError

from coalesce_api import constants, exceptions, models, strategies


def get_health_insurance_details(
    url: str, member_id: str
) -> models.HealthInsuranceDetails:
    try:
        response = requests.get(
            url, params={"member_id": member_id}, timeout=constants.TIMEOUT_SECONDS
        )
    except requests.exceptions.Timeout as e:
        raise exceptions.HealthInsuranceAPITimeout() from e
    try:
        health_insurance_details = models.HealthInsuranceDetails(**response.json())
    except ValidationError as e:
        raise exceptions.HealthInsuranceAPIValidationError() from e
    return health_insurance_details


def get_coalesce_health_insurance(
    strategy: strategies.CoalesceStrategy, sources: list[str], member_id: str
) -> models.HealthInsuranceDetails:
    return strategy(
        [get_health_insurance_details(source, member_id) for source in sources]
    )
