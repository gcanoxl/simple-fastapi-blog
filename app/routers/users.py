from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.auth.auth_handler import signJWT
from app.db import get_db
from app.schemas import UserSchema

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserSchema, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "token": signJWT(new_user),
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if not db_user or db_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return {
        "id": db_user.id,
        "username": db_user.username,
        "token": signJWT(db_user),
    }
