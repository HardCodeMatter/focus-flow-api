from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase): ...


class TaskRead(TaskBase):
    id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(TaskBase):
    is_completed: bool
