from pydantic import BaseModel


class User(BaseModel):
    id: int | None
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
