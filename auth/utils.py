import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["type"] = "access"
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=15)

    return jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algorithm)

def decode_access_token(token:str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(days=7)

    return jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algorithm)


def hash_password(plain:str) -> str:
    return bcrypt.hashpw(plain.encode(),bcrypt.gensalt()).decode()

def verify_password(plain:str,hashed:str) -> bool:
    return bcrypt.checkpw(plain.encode(),hashed.encode())


