from fastapi import FastAPI

from coalesce_api import health_insurance

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/coalesce")
async def coalesce(member_id: str):
    sources = ["http://api1.com", "http://api2.com", "http://api3.com"]
    return health_insurance.get_coalesce_health_insurance(sources, member_id)
