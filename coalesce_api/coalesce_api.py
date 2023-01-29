from pydantic import BaseModel


class HealthInsuranceDetails(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int


def get_health_insurance_details(url: str, member_id: str) -> HealthInsuranceDetails:
    return HealthInsuranceDetails(deductible=1000, stop_loss=10000, oop_max=5000)
