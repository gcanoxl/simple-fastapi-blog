import fastapi
from fastapi import status

from app import db, models

models.Base.metadata.create_all(bind=db.engine)

app = fastapi.FastAPI()


from .routers.users import router

app.include_router(router, prefix="/api/users", tags=["users"])


@app.get(
    "/api/healthcheck",
    description="Healthcheck endpoint",
    status_code=status.HTTP_200_OK,
)
async def healthcheck():
    return {"status": "ok"}
