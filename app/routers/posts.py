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
async def posts_get_number(
    db: Session = Depends(get_db),
    limit: int | None = None,
    offset: int = 0,
):
    total_count = db.query(models.Post).count()
    if limit is None:
        return {"count": total_count}
    if limit > total_count:
        limit = total_count
    if limit + offset > total_count:
        raise HTTPException(
            status_code=400,
            detail="Offset + limit is greater than total number of posts",
        )
    db_posts = (
        db.query(models.Post).order_by(models.Post.id).offset(offset).limit(limit).all()
    )
    return {
        "count": len(db_posts),
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "views": post.views,
            }
            for post in db_posts
        ],
    }


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


@router.put("/{post_id}", status_code=status.HTTP_200_OK)
async def posts_update(
    post_id: int,
    post: PostSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin"
        )
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.query(models.Post).filter(models.Post.id == post_id).update(
        {"title": post.title, "content": post.content}
    )
    db.commit()
    db.refresh(db_post)
    return {
        "id": db_post.id,
        "title": db_post.title,
        "content": db_post.content,
        "views": db_post.views,
    }
