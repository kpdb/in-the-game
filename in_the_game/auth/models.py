from pydantic import BaseModel, Field, EmailStr


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str


class TokenResponse(BaseModel):
    access_token: str
