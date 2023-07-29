from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.auth.auth_bearer import JWTBearer
from app.db import get_db
from app.schemas import PostSchema, UserSchema

router = APIRouter()

jwt_bearer = JWTBearer()


def get_current_user(
    db: Session = Depends(get_db),
    user: UserSchema = Depends(jwt_bearer),
) -> UserSchema:
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_add(
    post: PostSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not admin")
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "views": new_post.views,
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def posts_get_number(db: Session = Depends(get_db)):
    count = db.query(models.Post).count()
    return {"count": count}


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def posts_get(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "views": post.views,
    }
