from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from rest.auth.login import TokenSchema, get_current_user, user_login
from rest.auth.user import UserCreate, create_user, get_user
from rest.climbs.climb import GymClimb, create_climb, get_climbs
from rest.climbs.training_session import TrainingSession, create_training_session
from rest.database import pool

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


@app.on_event("startup")
async def open_pool():
    await pool.open()


@app.on_event("shutdown")
async def close_pool():
    await pool.close()


@app.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await user_login(form_data)


@app.post("/signup", summary="Create new user", response_model=dict)
async def create_new_user(user: UserCreate):
    return await create_user(user)


@app.get("/api/users/me", summary="Get user details", response_model=dict)
async def get_user_details(user=Depends(get_current_user)):
    return await get_user(user.id)


@app.post("/api/training-sessions", summary="Create new training session", response_model=dict)
async def create_user_training_session(training_session: TrainingSession, user=Depends(get_current_user)):
    return await create_training_session(user_id=user.id, training_session=training_session)


@app.get("/api/climbs", summary="Get user climbs", response_model=dict)
async def get_user_climbs(user=Depends(get_current_user)):
    return await get_climbs(user.id)


@app.post("/api/climbs", summary="Create a new climb", response_model=dict)
async def create_new_climb(climb: GymClimb, user=Depends(get_current_user)):
    return await create_climb(user_id=user.id, climb=climb)
