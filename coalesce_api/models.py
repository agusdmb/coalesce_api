from pydantic import BaseModel


class HealthInsuranceDetails(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int
