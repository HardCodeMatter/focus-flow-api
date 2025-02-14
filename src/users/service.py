from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.repository import UserRepository
from users.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def create(self, user_data: UserCreate) -> User:
        if await self.repository.user_exists_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This username is unavailable..'
            )
        
        if await self.repository.user_exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This email is unavailable.'
            )
        
        return await self.repository.create(user_data)

    async def get_by_id(self, user_id: str) -> User:
        if not await self.repository.user_exists_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User is not found.'
            )
        
        return await self.repository.get_by_id(user_id)
    
    async def get_by_username(self, username: str) -> User:
        if not await self.repository.user_exists_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User is not found.'
            )
        
        return await self.repository.get_by_username(username)

    async def update(self, user_id: str, user_data: UserUpdate) -> User:
        if not await self.repository.user_exists_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User is not found.'
            )
        
        user: User = await self.repository.get_by_id(user_id)

        return await self.repository.update(user, user_data)
    
    async def delete(self, user_id: str) -> dict:
        if not await self.repository.user_exists_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User is not found.'
            )
        
        user: User = await self.repository.get_by_id(user_id)
        await self.repository.delete(user)

        return {
            'detail': f"User '{user.username}' is successful deleted.",
        }
