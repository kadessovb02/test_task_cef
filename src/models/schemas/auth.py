from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., example="bek")
    password: str = Field(..., example="secret")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
