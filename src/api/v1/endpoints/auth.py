from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.services.auth_service import login_and_get_token
from src.models.schemas.auth import Token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = login_and_get_token(form_data.username, form_data.password)
    return token
