from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr, model_validator

from models.employee import EmployeeRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    token : str
    refresh_token : str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    sub: str
    email: str | None = None
    type: str | None = None
    role: EmployeeRole

class TokenRefresh(BaseModel):
    refresh_token:str

class AccessToken(BaseModel):
    access_token : str
    token_type: str = "bearer"