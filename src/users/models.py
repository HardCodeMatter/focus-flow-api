import typing
import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if typing.TYPE_CHECKING:
    from tasks.models import Task


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    fullname: Mapped[str] = mapped_column(nullable=True)
    
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    tasks: Mapped[list['Task']] = relationship(back_populates='owner')

    def __str__(self) -> str:
        return f'User(id="{self.id}", username="{self.username}", is_active={self.is_active}, is_verified={self.is_verified}, is_superuser={self.is_superuser},)'
    
    def __repr__(self) -> str:
        return self.__str__()
