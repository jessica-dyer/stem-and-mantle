import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "123456fdafds")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "123456fdafds")  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        expires = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[int] = None) -> str:
    if expires_delta:
        expires = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    expires = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
