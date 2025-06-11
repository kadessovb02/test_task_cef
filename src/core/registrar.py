from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.router import v1
from src.services.face_service import face_service
from src.scripts.seed_users import seed


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading face embeddings from %s", settings.faces_db_path)
    face_service.preload_faces()
    logger.info("Faces loaded: %d", len(face_service.list_faces()))
    if settings.seed_db:
        seed()
    yield  
    logger.info("Shutting down application")

def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
def register_router(app: FastAPI):
    app.include_router(v1)

def register_app():
    app = FastAPI(
        title=settings.title,
        version=settings.version,
        description=settings.description,
        openapi_prefix=settings.openapi_prefix,
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan
    )
    register_middleware(app)
    register_router(app)
    return app
