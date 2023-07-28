from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import PostSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def post_add(post: PostSchema, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
