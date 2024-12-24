from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None

    @field_validator('title', mode='before')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if value is None:
            return value

        return cls.validate_length(value, 'Title', 3, 30)

    @field_validator('description', mode='before')
    @classmethod
    def validate_description(cls, value: str) -> str:
        if value is None:
            return value

        return cls.validate_length(value, 'Description', 0, 200)
    
    @staticmethod
    def validate_length(value: str, field_name: str, min_length: int, max_length: int) -> str:
        if len(value.strip()) < min_length or len(value.strip()) > max_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{field_name} length must be between {min_length} and {max_length} characters.',
            )

        return value


class TaskRead(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase): ...


class TaskUpdate(TaskBase):
    is_completed: bool | None = None
