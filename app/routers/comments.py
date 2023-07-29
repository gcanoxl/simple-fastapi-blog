from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.routers.users import get_current_user
from app.schemas import CommentSchema, UserSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def comments_get_list(
    post_id: int,
    db: Session = Depends(get_db),
):
    db_comments = (
        db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    )
    return {
        "count": len(db_comments),
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
            }
            for comment in db_comments
        ],
    }


@router.put("/{comment_id}", status_code=status.HTTP_200_OK)
async def comment_update(
    comment_id: int,
    comment: CommentSchema,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )
    if db_comment.user_id != user.id and not user.is_admin:  # pyright: ignore
        raise HTTPException(
            status_code=403,
            detail="User is not comment owner",
        )
    db.query(models.Comment).filter(models.Comment.id == comment_id).update(
        {
            "content": comment.content,
        }
    )
    db.commit()
    db.refresh(db_comment)
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "user_id": db_comment.user_id,
    }


# @router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
