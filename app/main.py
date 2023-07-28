import fastapi
from fastapi import status

from app import db, models

models.Base.metadata.create_all(bind=db.engine)

app = fastapi.FastAPI()

from app.routers.posts import router as posts_router
from app.routers.users import router as users_router

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(posts_router, prefix="/api/posts", tags=["posts"])


@app.get(
    "/api/healthcheck",
    description="Healthcheck endpoint",
    status_code=status.HTTP_200_OK,
)
async def healthcheck():
    return {"status": "ok"}
