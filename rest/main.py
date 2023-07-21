import asyncpg
from fastapi import Depends, FastAPI

from auth.login import login_user
from auth.user import UserCreate, create_user, get_user
from climbs.climb import GymClimb, create_climb, get_climbs
from config import SQLALCHEMY_DATABASE_URI

app = FastAPI()


# Create a database connection pool
async def create_db_pool():
    return await asyncpg.create_pool(SQLALCHEMY_DATABASE_URI)


@app.on_event("startup")
async def startup_db():
    app.state.db_pool = await create_db_pool()


@app.on_event("shutdown")
async def shutdown_db():
    await app.state.db_pool.close()


@app.post("/login")
def login(username: str, password: str):
    return login_user(username, password)


@app.post("/users/", response_model=dict)
async def create_new_user(user: UserCreate, db: asyncpg.Pool = Depends(create_db_pool)):
    return await create_user(user, db)


@app.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int, db: asyncpg.Pool = Depends(create_db_pool)):
    return await get_user(user_id, db=db)


@app.get("/users/{user_id}/climbs", response_model=dict)
async def get_user_climbs(user_id: int, db: asyncpg.Pool = Depends(create_db_pool)):
    return await get_climbs(user_id, db)


@app.post("/climbs/", response_model=dict)
async def create_new_climb(climb: GymClimb, db: asyncpg.Pool = Depends(create_db_pool)):
    return await create_climb(climb, db)
