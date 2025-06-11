from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.security import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def require_auth(user = Depends(get_current_user)):
    return user
