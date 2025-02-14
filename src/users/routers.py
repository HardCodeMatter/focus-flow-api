from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from users.models import User
from users.schemas import Token, UserCreate
from users.service import UserService
from users.utils import authenticate_user, create_access_token


router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user: User = await authenticate_user(session, form_data.username, form_data.password)
    access_token: str = create_access_token(user.username)
    
    return Token(
        access_token=access_token,
        token_type='bearer',
    )


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    await UserService(session).create(user_data)

    return {
        'detail': 'User is successful created.'
    }
