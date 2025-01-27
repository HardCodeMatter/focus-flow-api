import uuid
from enum import Enum
from datetime import datetime

from sqlalchemy import ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    related_tags: Mapped[list['Tag']] = relationship(
        secondary='task_tags',
        back_populates='related_tasks',
    )

    def __str__(self) -> str:
        return f'Task(id="{self.id}", title="{self.title}", is_completed="{self.is_completed}", priority="{self.priority}")'

    def __repr__(self) -> str:
        return self.__str__()


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    related_tasks: Mapped[list['Task']] = relationship(
        secondary='task_tags',
        back_populates='related_tags',
    )

    def __str__(self) -> str:
        return f'Tag(id="{self.id}", title="{self.title}")'

    def __repr__(self) -> str:
        return self.__str__()


class TaskTag(Base):
    __tablename__ = 'task_tags'

    task_id: Mapped[str] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        primary_key=True,
    )
    tag_id: Mapped[str] = mapped_column(
        ForeignKey('tags.id', ondelete='CASCADE'),
        primary_key=True,
    )

    def __str__(self) -> str:
        return f'TaskTag(task_id="{self.task_id}", tag_id="{self.tag_id}")'

    def __repr__(self) -> str:
        return self.__str__()
