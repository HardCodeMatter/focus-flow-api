import re
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    fullname: str | None = None
    username: str | None = None
    email: str

    @field_validator('fullname')
    @classmethod
    def validate_fullname(cls, value: str) -> str:
        if value is None:
            return value
        
        if not re.match(r'^[A-Za-z]+(\.?)(( [A-Za-z]+(\.?)?)+)?$', value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Fullname is not matching the pattern.'
            )

        return cls.validate_length(value, 'Fullname', 0, 64)

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if value is None:
            return value
        
        if not re.match(r'^(?!.*\.\.)([A-Za-z0-9_][A-Za-z0-9._]{1,28}[A-Za-z0-9_])$', value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username is not matching the pattern.'
            )

        return cls.validate_length(value, 'Username', 3, 30)

    @staticmethod
    def validate_length(value: str, field_name: str, min_length: int, max_length: int) -> str:
        if not (min_length <= len(value.strip()) <= max_length):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{field_name} length must be between {min_length} and {max_length} characters.',
            )

        return value


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


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(UserBase): ...
