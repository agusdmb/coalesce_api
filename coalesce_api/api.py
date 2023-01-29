from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/coalesce")
async def coalesce(member_id: str):
    return member_id
