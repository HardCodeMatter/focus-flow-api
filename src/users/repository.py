from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import UserCreate, UserUpdate
from users.utils import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_data: UserCreate) -> User:
        user_data.hashed_password = hash_password(user_data.hashed_password)
        user: User = User(**user_data.model_dump())

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def get_by_id(self, user_id: str) -> User:
        stmt: Select[User] = select(User).filter_by(id=user_id)
        user: User = (
            await self.session.execute(stmt)
        ).scalar_one()

        return user
    
    async def get_by_username(self, username: str) -> User:
        stmt: Select[User] = select(User).filter_by(username=username)
        user: User = (
            await self.session.execute(stmt)
        ).scalar_one()

        return user
    
    async def update(self, user: User, user_data: UserUpdate) -> User:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def delete(self, user: User) -> bool:
        await self.session.delete(user)
        await self.session.commit()

        return True
    
    async def user_exists_by_id(self, user_id: str) -> bool:
        stmt: Select[User] = select(User).filter_by(id=user_id)
        user: User = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return user is not None
    
    async def user_exists_by_username(self, username: str) -> bool:
        stmt: Select[User] = select(User).filter_by(username=username)
        user: User = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return user is not None
    
    async def user_exists_by_email(self, email: str) -> bool:
        stmt: Select[User] = select(User).filter_by(email=email)
        user: User = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return user is not None
