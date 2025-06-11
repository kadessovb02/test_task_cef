from __future__ import annotations
from pathlib import Path
from typing import List, Optional

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from src import PROJECT_ROOT


class Settings(BaseSettings):
    title: Optional[str]
    description: Optional[str]
    openapi_prefix: Optional[str]
    version: Optional[str]
    debug: bool = False

    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/api"

    cors_allowed_origins: List[str] = ["*"]

    database_url: AnyUrl

    faces_db_path: Path = PROJECT_ROOT / "faces_db"
    seed_db: bool = False

    face_detector_prototxt: Path = PROJECT_ROOT / "src" / "ml_models" / "deploy.prototxt"
    face_detector_model:    Path = PROJECT_ROOT / "src" / "ml_models" / "res10_300x300_ssd_iter_140000.caffemodel"
    face_embedder_model:    Path = PROJECT_ROOT / "src" / "ml_models" / "nn4.small2.v1.t7"
    
    access_token_expire_minutes: int
    jwt_secret_key: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
