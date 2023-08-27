
import asyncpg
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from utils import get_hashed_password


class UserCreate(BaseModel):
    username: EmailStr
    password: str


class UserAuth(BaseModel):
    username: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    id: int
    username: str


class SystemUser(UserOut):
    password: str


async def get_user(user_id: int, db: asyncpg.Pool = Depends()):
    query = "SELECT id, username, created_at, updated_at FROM users WHERE id = $1"
    try:
        result = await db.fetchrow(query, user_id)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": result["id"],
            "username": result["username"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}") from e


async def create_user(user_data: UserCreate, db: asyncpg.Pool = Depends()):
    query = "SELECT id, username FROM users WHERE username = $1"
    user = await db.fetchrow(query, user_data.username)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    username = user_data.username
    hashed_password = get_hashed_password(user_data.password)

    query = "INSERT INTO users (username, password, created_at, updated_at) VALUES ($1, $2, DEFAULT, DEFAULT) RETURNING id, username, created_at, updated_at"
    try:
        result = await db.fetchrow(query, username, hashed_password)
        return {
            "id": result["id"],
            "username": result["username"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") from e
