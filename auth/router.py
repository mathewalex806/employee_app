
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import service as auth_service
from sqlalchemy.ext.asyncio import AsyncSession


from auth.utils import create_access_token, verify_password
from database.connection import get_db
from exceptions.handlers import NotFoundException, UnauthorizedException
from auth.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    employee = await auth_service.login(db, body.email)
    if employee is None:
        raise NotFoundException("User not found")
    
    if not verify_password(plain=body.password, hashed=employee.password_hash):
        raise UnauthorizedException("User password does not match")
    
    token = create_access_token({"id": employee.id, "email": employee.email})
    return TokenResponse(token=token)