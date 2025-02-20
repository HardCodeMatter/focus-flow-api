from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError, PyJWTError
from passlib.context import CryptContext
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_async_session
from users import service
from users.models import User
from users.schemas import TokenData


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def hash_password(plain_password: str) -> str:
    return password_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, username: str, plain_password: str) -> User:
    user: User = await service.UserService(session).get_by_username(username)

    if not verify_password(plain_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.'
        )
    
    return user


def create_access_token(username: str) -> str:
    encode: dict = {'sub': username}
    expires: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({'exp': expires})

    return jwt.encode(encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)


def create_refresh_token(username: str) -> str:
    encode: dict = {'sub': username}
    expires: datetime = datetime.now(timezone.utc) + timedelta(days=settings.AUTH_REFRESH_TOKEN_EXPIRE_DAYS)
    encode.update({'exp': expires})

    return jwt.encode(encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)


def decode_refresh_token(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(
            refresh_token,
            key=settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )

        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token.'
        )


async def get_current_user(
    token: str = Security(oauth2_bearer),
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            raise credentials_exception
        
        token_data: TokenData = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    return await service.UserService(session).get_by_username(token_data.username)


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is not active.'
        )
    
    return current_user
