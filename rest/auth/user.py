from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from rest.database import db_execute_one
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


async def get_user(user_id: int):
    print("i am in the get user function")
    query = "SELECT id, username, created_at, updated_at FROM users WHERE id = %(user_id)s"
    try:
        args = {"user_id": user_id}
        print(user_id)
        result = await db_execute_one(query=query, args=args)
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


async def create_user(user_data: UserCreate):
    query = "SELECT id, username FROM users WHERE username = %(username)s"
    args = {"username": user_data.username}
    user = await db_execute_one(query=query, args=args)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    username = user_data.username
    hashed_password = get_hashed_password(user_data.password)

    query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (%(username)s, %(password)s, DEFAULT, DEFAULT) RETURNING id, username, created_at, updated_at"
    args = {"username": username, "password": hashed_password}
    try:
        result = await db_execute_one(query=query, args=args)
        if result:
            return {
                "id": result["id"],
                "username": result["username"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") from e
