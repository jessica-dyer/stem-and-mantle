import asyncpg
from fastapi import Depends, HTTPException
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: EmailStr
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


async def create_user(user: UserCreate, db: asyncpg.Pool = Depends()):
    query = "INSERT INTO users (username, password, created_at, updated_at) VALUES ($1, $2, DEFAULT, DEFAULT) RETURNING id, username, created_at, updated_at"
    try:
        result = await db.fetchrow(query, user.username, user.password)
        return {
            "id": result["id"],
            "username": result["username"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") from e
