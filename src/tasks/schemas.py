from enum import Enum
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator

from .models import Priority, TaskStatus


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None
   
    priority: 'Priority' = Priority.low
    due_date: datetime | None = None

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
    
    @field_validator('priority', mode='before')
    @classmethod
    def validate_priority(cls, value: str) -> str:
        if value not in Priority.__members__.values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unknown value \'{value}\' for priority.',
            )
        
        return value
    
    @field_validator('due_date', mode='before')
    @classmethod
    def validate_datetime(cls, value: datetime | None):
        if value is None:
            return value
        
        try:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Mismatching datetime format. It should be YYYY-MM-DDTHH:MM:SS.'
            )

    @field_validator('due_date', mode='after')
    @classmethod
    def validate_due_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value

        if value <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Due date cannot be less than or equal to current date.',
            )
        
        return value

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
    status: TaskStatus
    priority: Priority
    related_tags: list['TagRead'] = []
    created_at: datetime
    updated_at: datetime
    due_date: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskCreate(TaskBase): ...


class TaskUpdate(TaskBase):
    status: TaskStatus = TaskStatus.ongoing

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in TaskStatus.__members__.values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unknown value for status.',
            )
        
        return value


class SortBy(Enum):
    priority: str = 'priority'
    created_at: str = 'created_at'
    status: str = 'status'


class Order(Enum):
    asc: str = 'asc'
    desc: str = 'desc'


class TaskQueryParams(BaseModel):
    sort_by: SortBy = SortBy.priority
    order: Order = Order.desc


class TagBase(BaseModel):
    title: str

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if value is None:
            return value
        
        return cls.validate_length(value, 'Title', 2, 10)

    @staticmethod
    def validate_length(value: str, field_name: str, min_length: int, max_length: int) -> str:
        if not (min_length <= len(value.strip()) <= max_length):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{field_name} length must be between {min_length} and {max_length} characters.',
            )
        
        return value


class TagRead(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class TagCreate(TagBase): ...


class TagUpdate(TagBase): ...
