from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None
    email: str
    username: str
    password: str
    is_admin: bool | None
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_mode = True
