from fastapi import APIRouter

from app.models import UserSchema

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/")
async def user_signup(user: UserSchema) -> dict:
    return user.model_dump()
