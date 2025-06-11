import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.repositories.user_repo import UserRepo
from src.models.domain.user import User

@pytest.fixture
def user_repo():
    repo = UserRepo()
    repo._engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    repo._metadata.create_all(repo._engine)
    return repo

def test_create_user_success(user_repo):
    user_repo.create_user("alice", "hashed_pwd", "Alice Smith")
    user = user_repo.get_by_username("alice")
    assert user.username == "alice"
    assert user.hashed_password == "hashed_pwd"
    assert user.full_name == "Alice Smith"
    assert user.disabled is False

def test_create_user_duplicate(user_repo):
    user_repo.create_user("bob", "pwd", "Bob")
    with pytest.raises(ValueError) as exc_info:
        user_repo.create_user("bob", "pwd2")
    assert "already exists" in str(exc_info.value)

def test_get_nonexistent_user(user_repo):
    user = user_repo.get_by_username("nonexistent")
    assert user is None
