import typing
import uuid
from enum import Enum
from datetime import datetime

from sqlalchemy import ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if typing.TYPE_CHECKING:
    from users.models import User


class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class TaskStatus(str, Enum):
    ongoing = 'ongoing'
    completed = 'completed'
    overdue = 'overdue'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(SQLAlchemyEnum(TaskStatus), server_default=TaskStatus.ongoing, nullable=False)
    priority: Mapped[str] = mapped_column(SQLAlchemyEnum(Priority), server_default=Priority.low, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    due_date: Mapped[datetime] = mapped_column(nullable=True)

    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    owner: Mapped['User'] = relationship(back_populates='tasks')

    comments: Mapped[list['Comment']] = relationship(back_populates='task')

    related_tags: Mapped[list['Tag']] = relationship(
        secondary='task_tags',
        back_populates='related_tasks',
    )

    def __str__(self) -> str:
        return f'Task(id="{self.id}", title="{self.title}", status="{self.status}", priority="{self.priority}")'

    def __repr__(self) -> str:
        return self.__str__()


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    owner: Mapped['User'] = relationship(back_populates='tags')

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


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    comment: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)

    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship(back_populates='comments')

    task_id: Mapped[str] = mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'))
    task: Mapped['Task'] = relationship(back_populates='comments')

    def __str__(self) -> str:
        return f'Comment(id="{self.id}", comment={self.comment}, user_id="{self.user_id}", task_id="{self.task_id}")'
    
    def __repr__(self) -> str:
        return self.__str__()
