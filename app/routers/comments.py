from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.routers.users import get_current_user
from app.schemas import CommentSchema, UserSchema

router = APIRouter()


@router.post("/", status_code=201)
async def comment_add(
    comment: CommentSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )
    new_comment = models.Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=user.id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {
        "id": new_comment.id,
        "content": new_comment.content,
        "post_id": new_comment.post_id,
        "user_id": new_comment.user_id,
    }
