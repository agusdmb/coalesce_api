from fastapi import FastAPI, HTTPException, status

from coalesce_api import constants, exceptions, health_insurance

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/coalesce")
async def coalesce(member_id: str):
    try:
        return health_insurance.get_coalesce_health_insurance(
            constants.SOURCES, member_id
        )
    except exceptions.HealthInsuranceAPITimeout as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Source timeout"
        ) from e
    except exceptions.HealthInsuranceAPIValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Source data corrupted",
        ) from e
