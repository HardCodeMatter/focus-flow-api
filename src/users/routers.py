from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_async_session
from users.models import User
from users.schemas import Token, UserCreate
from users.service import UserService
from users.utils import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    decode_refresh_token
)


router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = Response(),
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user: User = await authenticate_user(session, form_data.username, form_data.password)
    
    access_token: str = create_access_token(user.username)
    refresh_token: str = create_refresh_token(user.username)

    response.set_cookie(key='refresh_token', value=refresh_token, max_age=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS, httponly=True)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
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


@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Request = Request,
    response: Response = Response()
) -> Token:
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is not provided.'
        )
    
    payload = decode_refresh_token(refresh_token)

    access_token = create_access_token(payload['sub'])
    refresh_token = create_refresh_token(payload['sub'])

    response.set_cookie(key='refresh_token', value=refresh_token, max_age=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS, httponly=True, secure=True, samesite='strict')

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )
