from pydantic import BaseModel
import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    email: str | None = None


class UserUpdate(BaseModel):
    id: int
    new_username: str | None = None
    email: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    email: str | None
    updated_at: datetime.datetime

