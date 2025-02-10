from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    fullname: str
    username: str
    email: str


class UserRead(BaseModel):
    id: str
    fullname: str
    username: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase): ...


class UserUpdate(UserBase): ...
