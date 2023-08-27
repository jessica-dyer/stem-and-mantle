from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from jose.exceptions import JWTError
from pydantic import BaseModel, ValidationError

from rest.auth.user import UserOut
from rest.database import db_execute_one
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY,
    create_access_token,
    create_refresh_token,
    verify_password,
)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    exp: int


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


class SystemUser(UserOut):
    password: str


async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = "SELECT username, password FROM users WHERE username = %(username)s"
    args = {"username": form_data.username}
    user = await db_execute_one(query=query, args=args)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    hashed_pass = user["password"]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"]),
    }


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    query = "SELECT id, username, password FROM users WHERE username = %(username)s"
    args = {"username": token_data.sub}
    user = await db_execute_one(query=query, args=args)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(**user)
