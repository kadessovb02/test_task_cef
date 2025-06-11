from fastapi import APIRouter

from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.identify import router as identify_router

v1 = APIRouter()

v1.include_router(auth_router)
v1.include_router(identify_router)
