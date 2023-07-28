from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import UserSchema

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserSchema, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
    }
