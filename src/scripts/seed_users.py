from src.repositories.user_repo import user_repo
from src.utils.hashing import hash_password

def seed():
    users = [
        {"username": "bek", "password": "secret", "full_name": "Bek Kadessov"},
    ]
    for u in users:
        hashed = hash_password(u["password"])
        user_repo.create_user(
            username=u["username"],
            hashed_password=hashed,
            full_name=u["full_name"],
            disabled=False
        )
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
