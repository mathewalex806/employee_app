from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr, model_validator


class LoginRequest(BaseModel):
    email : str 
    password : str = Field(min_length=6)


class TokenResponse(BaseModel):
    token : str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str