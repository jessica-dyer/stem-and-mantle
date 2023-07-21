import jwt
from fastapi import HTTPException

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def login_user(username: str, password: str):
    # In a real application, you would compare the username and password
    # against a user database or user storage mechanism.
    # For this example, we assume a hardcoded username and password.

    if username == "testuser" and password == "password":
        # Generate an access token (e.g., JWT) to be used for subsequent requests
        access_token = create_access_token(username)
        return {"access_token": access_token, "token_type": "bearer"}

    # If the provided credentials are incorrect, raise an HTTPException with 401 status code.
    raise HTTPException(status_code=401, detail="Invalid credentials")


def create_access_token(data: dict):
    # Create and return a JWT token containing the user data.
    return jwt.JWT.encode(data, SECRET_KEY)
