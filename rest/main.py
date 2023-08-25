
import asyncpg
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.login import login_user
from auth.user import UserCreate, create_user, get_user
from climbs.climb import GymClimb, create_climb, get_climbs
from climbs.training_session import TrainingSession, create_training_session
from config import DATABASE_URL

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)


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


@app.post("/training_sessions/", response_model=dict)
async def create_user_training_session(training_session: TrainingSession, db: asyncpg.Pool = Depends(create_db_pool)):
    return await create_training_session(training_session, db)


@app.get("/users/{user_id}/climbs", response_model=dict)
async def get_user_climbs(user_id: int, db: asyncpg.Pool = Depends(create_db_pool)):
    return await get_climbs(user_id, db)


@app.post("/climbs/", response_model=dict)
async def create_new_climb(climb: GymClimb, db: asyncpg.Pool = Depends(create_db_pool)):
    return await create_climb(climb, db)
