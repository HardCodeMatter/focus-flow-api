import uuid
from enum import Enum
from datetime import datetime

from sqlalchemy import func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    is_completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[str] = mapped_column(SQLAlchemyEnum(Priority), server_default=Priority.low, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __str__(self) -> str:
        return f'Task(id="{self.id}", title="{self.title}", is_completed="{self.is_completed}", priority="{self.priority}")'

    def __repr__(self) -> str:
        return self.__str__()
