import asyncpg
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from auth.login import TokenSchema, get_current_user, user_login
from auth.user import UserCreate, UserOut, create_user, get_user
from climbs.climb import GymClimb, create_climb, get_climbs
from climbs.training_session import TrainingSession, create_training_session
from config import DATABASE_URL

description = """
# Stem and Mantle Climbing Training API 🧗‍♀️🧗‍♂️

Welcome to the Stem and Mantle Climbing Training API – your gateway to climbing training data and analytics.
Elevate your climbing skills and track your progress using this robust API designed for climbers.

## Features

With the Stem and Mantle Climbing Training API, you can:

- Create and manage user profiles to store your climbing journey.
- Record training sessions.
- Keep a comprehensive log of your climbing sessions, routes, and achievements.

## Endpoints

### Users

- **Create User**: Create a new user profile to start your climbing journey.
- **Read User**: Retrieve user details, training history, and climbing statistics.

### Training Sessions

- **Create Training Session**: Log your training sessions to track your climbing-specific workouts.
- **Get User Climbs**: Access your training session data to monitor your training progress.

### Climbs

- **Create Climb**: Record your climbing achievements and challenges.
- **Get User Climbs**: Retrieve information about the climbs you've conquered.

"""

app = FastAPI(
    title="Stem and Mantle",
    description=description,
    summary="",
    version="0.0.1",
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


async def create_db_connection():
    return await asyncpg.connect(DATABASE_URL)


@app.on_event("startup")
async def startup_db():
    app.state.db_connection = await create_db_connection()


@app.on_event("shutdown")
async def shutdown_db():
    await app.state.db_connection.close()


@app.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: asyncpg.Pool = Depends(create_db_connection)):
    return await user_login(form_data, db)


@app.post("/signup/", response_model=dict)
async def create_new_user(user: UserCreate, db: asyncpg.Pool = Depends(create_db_connection)):
    return await create_user(user, db)


@app.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int, db: asyncpg.Pool = Depends(create_db_connection)):
    return await get_user(user_id, db=db)


@app.post("/training_sessions/", response_model=dict)
async def create_user_training_session(
    training_session: TrainingSession, db: asyncpg.Pool = Depends(create_db_connection)
):
    return await create_training_session(training_session, db)


@app.get("/users/{user_id}/climbs", response_model=dict)
async def get_user_climbs(user_id: int, db: asyncpg.Pool = Depends(create_db_connection)):
    return await get_climbs(user_id, db)


@app.post("/climbs/", response_model=dict)
async def create_new_climb(climb: GymClimb, db: asyncpg.Pool = Depends(create_db_connection)):
    return await create_climb(climb, db)


@app.get("/me", summary="Get details of currently logged in user", response_model=UserOut)
async def get_me(user=Depends(get_current_user)):
    return user
