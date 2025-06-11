from dataclasses import dataclass
from typing import Sequence


@dataclass(slots=True)
class FaceIdentity:
    person_id: str
    embedding: Sequence[float]
    
    def __repr__(self) -> str:
        return f"<FaceIdentity {self.person_id[:20]}...>"
