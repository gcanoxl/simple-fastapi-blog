import fastapi
from fastapi import status

app = fastapi.FastAPI()


@app.get(
    "/api/healthcheck",
    description="Healthcheck endpoint",
    status_code=status.HTTP_200_OK,
)
async def healthcheck():
    return {"status": "ok"}
