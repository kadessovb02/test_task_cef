from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.core.config import settings
from src.core.security import create_access_token
from src.models.domain.user import User as DomainUser
from src.models.schemas.auth import Token
from src.repositories.user_repo import user_repo
from src.utils.hashing import hash_password, verify_password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str) -> Optional[DomainUser]:
    user = user_repo.get_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_and_get_token(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    return Token(access_token=access_token)
