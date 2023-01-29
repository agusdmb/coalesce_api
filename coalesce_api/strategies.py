from typing import Callable, Sequence

from coalesce_api import exceptions, models

CoalesceStrategy = Callable[
    [Sequence[models.HealthInsuranceDetails]], models.HealthInsuranceDetails
]


def average_health_insurances(
    health_insurances: Sequence[models.HealthInsuranceDetails],
) -> models.HealthInsuranceDetails:
    if not health_insurances:
        raise exceptions.HealthInsuranceValueError(
            "Must provide at least one Health Insurance to compute average."
        )

    deductible_avg = 0
    stop_loss_avg = 0
    oop_max_avg = 0
    for health_insurance in health_insurances:
        deductible_avg += health_insurance.deductible
        stop_loss_avg += health_insurance.stop_loss
        oop_max_avg += health_insurance.oop_max
    return models.HealthInsuranceDetails(
        deductible=deductible_avg // len(health_insurances),
        stop_loss=stop_loss_avg // len(health_insurances),
        oop_max=oop_max_avg // len(health_insurances),
    )
