from fastapi import FastAPI

from coalesce_api import constants, health_insurance

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/coalesce")
async def coalesce(member_id: str):
    return health_insurance.get_coalesce_health_insurance(constants.SOURCES, member_id)
