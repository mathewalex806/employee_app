from fastapi import APIRouter, Depends, HTTPException
from auth import service as auth_service
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, decode_access_token
from database.connection import get_db
from auth.schemas import TokenRefresh, AccessToken
from fastapi.security import OAuth2PasswordRequestForm
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=AccessToken)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    logger.info(f"User {form.username} is logging in.")
    token = await auth_service.login(db, form.username, form.password)
    return AccessToken(access_token=token)


# @router.post("/login", response_model=TokenResponse)
# async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):

#     employee = await auth_service.login(db, body.email)
#     if employee is None:
#         raise NotFoundException("User not found")

#     if not verify_password(body.password, employee.password_hash):
#         raise UnauthorizedException("User password does not match")

#     payload = {
#         "sub": str(employee.id),
#         "email": employee.email
#     }

#     access_token = create_access_token(payload)
#     refresh_token = create_refresh_token(payload)

#     return TokenResponse(
#         token=access_token,
#         refresh_token=refresh_token
#     )


@router.post("/refresh")
async def refresh(body: TokenRefresh):

    payload = decode_access_token(body.refresh_token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    access_token = create_access_token(
        {"sub": payload["sub"], "email": payload["email"]}
    )

    return {"access_token": access_token}
