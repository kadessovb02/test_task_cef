from typing import Optional
from pydantic import BaseModel


class IdentifyResponse(BaseModel):
    matched: bool
    person_id: Optional[str] = None

    class Config:
        schema_extra = {
            "examples": [
                {"matched": True, "person_id": "john_doe"},
                {"matched": False, "person_id": None},
            ]
        }
