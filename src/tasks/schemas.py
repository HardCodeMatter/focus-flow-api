from enum import Enum
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator

from .models import Priority, TaskStatus


class TaskStatus(str, Enum):
    ongoing = 'ongoing'
    completed = 'completed'
    overdue = 'overdue'


class TaskBase(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: 'Priority' = Priority.low

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

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskCreate(TaskBase):
    related_tags: list[str]


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
