from __future__ import annotations

from typing import Optional

from sqlalchemy import exc 

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String,
    Boolean,
    create_engine,
    select,
    insert,
)
from src.core.config import settings
from src.models.domain.user import User


class UserRepo():
    _metadata = MetaData()
    _users = Table(
        "users",
        _metadata,
        Column("username", String, primary_key=True, nullable=False),
        Column("hashed_password", String, nullable=False),
        Column("full_name", String, nullable=True),
        Column("disabled", Boolean, nullable=False, default=False),
    )

    def __init__(self) -> None:  
        self._engine = create_engine(str(settings.database_url), echo=False, future=True)
        self._metadata.create_all(self._engine)

    def get_by_username(self, username: str) -> Optional[User]:
        with self._engine.connect() as conn:
            stmt = select(self._users).where(self._users.c.username == username)
            row = conn.execute(stmt).fetchone()
            if row is None:
                return None
            return User(
                username=row.username,
                hashed_password=row.hashed_password,
                full_name=row.full_name,
                disabled=row.disabled,
            )
        
    def create_user(
        self,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        disabled: bool = False,
    ) -> None:
        stmt = insert(self._users).values(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            disabled=disabled,
        )
        try:
            with self._engine.begin() as conn:
                conn.execute(stmt)
        except exc.IntegrityError as e:
            raise ValueError(f"User '{username}' already exists") from e

user_repo = UserRepo()
