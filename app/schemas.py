from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    username: str
    password: str | None = None
    is_admin: bool | None = False


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    title: str
    content: str
    views: int | None = 0
