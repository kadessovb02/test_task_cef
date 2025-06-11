from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class User:
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    disabled: bool = False

    def is_active(self) -> bool:
        return not self.disabled
