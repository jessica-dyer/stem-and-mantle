import logging
from datetime import date
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator

from rest.climbs.constants import CLIMBING_GRADE_SCORES
from rest.database import db_execute_one, query_database_many

logger = logging.getLogger()


class GradeEnum(str, Enum):
    GRADE_5_0 = "5.0"
    GRADE_5_1 = "5.1"
    GRADE_5_2 = "5.2"
    GRADE_5_3 = "5.3"
    GRADE_5_4 = "5.4"
    GRADE_5_5 = "5.5"
    GRADE_5_6 = "5.6"
    GRADE_5_7 = "5.7"
    GRADE_5_7_PLUS = "5.7+"
    GRADE_5_8_MINUS = "5.8-"
    GRADE_5_8 = "5.8"
    GRADE_5_8_PLUS = "5.8+"
    GRADE_5_9_MINUS = "5.9-"
    GRADE_5_9 = "5.9"
    GRADE_5_9_PLUS = "5.9+"
    GRADE_5_10_A = "5.10a"
    GRADE_5_10_MINUS = "5.10-"
    GRADE_5_10_A_B = "5.10a/b"
    GRADE_5_10_B = "5.10b"
    GRADE_5_10 = "5.10"
    GRADE_5_10_B_C = "5.10b/c"
    GRADE_5_10_C = "5.10c"
    GRADE_5_10_PLUS = "5.10+"
    GRADE_5_10_C_D = "5.10c/d"
    GRADE_5_10_D = "5.10d"
    GRADE_5_11_A = "5.11a"
    GRADE_5_11_MINUS = "5.11-"
    GRADE_5_11_A_B = "5.11a/b"
    GRADE_5_11_B = "5.11b"
    GRADE_5_11 = "5.11"
    GRADE_5_11_B_C = "5.11b/c"
    GRADE_5_11_C = "5.11c"
    GRADE_5_11_PLUSE = "5.11+"
    GRADE_5_11_C_D = "5.11c/d"
    GRADE_5_11_D = "5.11d"
    GRADE_5_12_A = "5.12a"
    GRADE_5_12_MINUS = "5.12-"
    GRADE_5_12_A_B = "5.12a/b"
    GRADE_5_12_B = "5.12b"
    GRADE_5_12 = "5.12"
    GRADE_5_12_B_C = "5.12b/c"
    GRADE_5_12_C = "5.12c"
    GRADE_5_12_PLUS = "5.12+"
    GRADE_5_12_C_D = "5.12c/d"
    GRADE_5_12_D = "5.12d"
    GRADE_5_13_A = "5.13a"
    GRADE_5_13_MINUS = "5.13-"
    GRADE_5_13_A_B = "5.13a/b"
    GRADE_5_13_B = "5.13b"
    GRADE_5_13 = "5.13"
    GRADE_5_13_B_C = "5.13b/c"
    GRADE_5_13_C = "5.13c"
    GRADE_5_13_PLUS = "5.13+"
    GRADE_5_13_C_D = "5.13c/d"
    GRADE_5_13_D = "5.13d"
    GRADE_5_14_A = "5.14a"
    GRADE_5_14_MINUS = "5.14-"
    GRADE_5_14_A_B = "5.14a/b"
    GRADE_5_14_B = "5.14b"
    GRADE_5_14 = "5.14"
    GRADE_5_14_B_C = "5.14b/c"
    GRADE_5_14_C = "5.14c"
    GRADE_5_14_PLUS = "5.14+"
    GRADE_5_14_C_D = "5.14c/d"
    GRADE_5_14_D = "5.14d"
    GRADE_5_15_A = "5.15a"
    GRADE_5_15_MINUS = "5.15-"
    GRADE_5_15_A_B = "5.15a/b"
    GRADE_5_15_B = "5.15b"
    GRADE_5_15 = "5.15"
    GRADE_5_15_C = "5.15c"
    GRADE_5_15_PLUS = "5.15+"
    GRADE_5_15_C_D = "5.15c/d"
    GRADE_5_15_D = "5.15d"
    GRADE_5_UNKNOWN = "5.?"


class Gym(Enum):
    VERTICAL_WORLD_SEATTLE = "Vertical World: Seattle"
    VERTICAL_WORLD_NORTH = "Vertical World: North"
    OTHER = "Other"


class ClimbingStyle(Enum):
    TOP_ROPE = "Top Rope"
    LEAD = "Lead"


class GymClimb(BaseModel):
    training_session_id: int
    gym: Gym
    date: date
    grade_rated: GradeEnum
    grade_feels: Optional[GradeEnum]
    style: ClimbingStyle
    number_of_takes: int
    completed: bool
    setter: str
    notes: Optional[str]

    @validator("grade_feels")
    def validate_grade_feels(cls, v):
        return v.value if v else None


async def get_climbs(user_id: int):
    query_user = "SELECT EXISTS (SELECT 1 FROM users WHERE id = %(user_id)s);"
    query_climbs = "SELECT * from climbs WHERE user_id = %(user_id)s;"
    args = {"user_id": user_id}
    user_exists = await query_database_many(query=query_user, args=args)
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        climbs = await query_database_many(query=query_climbs, args=args)
        if not climbs:
            return {"message": "User has no climbs"}
        data = [
            {
                "id": climb["id"],
                "user_id": climb["user_id"],
                "training_session_id": climb["training_session_id"],
                "date": climb["date"],
                "gym": climb["gym"],
                "style": climb["style"],
                "grade_rated": climb["grade_rated"],
                "grade_feels": climb["grade_feels"],
                "number_of_takes": climb["number_of_takes"],
                "completed": climb["completed"],
                "setter": climb["setter"],
                "notes": climb["notes"],
                "climb_score": climb["climb_score"],
            }
            for climb in climbs
        ]
        return {"climbs": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching climbs: {str(e)}") from e


async def create_climb(user_id: int, climb: GymClimb):
    climb_score = CLIMBING_GRADE_SCORES.get(climb.grade_rated.value, None)
    training_session_query = "SELECT * FROM training_sessions WHERE %(training_session_id)s = id;"
    training_session = await db_execute_one(
        query=training_session_query, args={"training_session_id": climb.training_session_id}
    )
    if not training_session:
        raise HTTPException(status_code=404, detail=f"Training session not found: {climb.training_session_id}")
    args = {
        "user_id": user_id,
        "training_session_id": training_session["id"],
        "gym": climb.gym.value,
        "date": training_session["date"],
        "grade_rated": climb.grade_rated.value,
        "grade_feels": climb.grade_feels,
        "style": climb.style.value,
        "number_of_takes": climb.number_of_takes,
        "completed": climb.completed,
        "setter": climb.setter,
        "notes": climb.notes,
        "climb_score": climb_score,
    }
    query = """
        INSERT INTO climbs (user_id, training_session_id, gym, date, grade_rated, grade_feels, style,
                            number_of_takes, completed, setter, notes, climb_score)
        VALUES (%(user_id)s, %(training_session_id)s, %(gym)s, %(date)s, %(grade_rated)s, %(grade_feels)s, %(style)s, %(number_of_takes)s, %(completed)s, %(setter)s, %(notes)s, %(climb_score)s)
        RETURNING id, training_session_id, user_id, gym, date, grade_rated, grade_feels, style,
                  number_of_takes, completed, setter, notes, climb_score
    """
    try:
        result = await db_execute_one(query=query, args=args)
        if result:
            return {
                "climb": {
                    "id": result["id"],
                    "user_id": result["user_id"],
                    "training_session_id": result["training_session_id"],
                    "date": result["date"],
                    "gym": result["gym"],
                    "style": result["style"],
                    "grade_rated": result["grade_rated"],
                    "grade_feels": result["grade_feels"],
                    "number_of_takes": result["number_of_takes"],
                    "completed": result["completed"],
                    "setter": result["setter"],
                    "notes": result["notes"],
                    "climb_score": result["climb_score"],
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating climb: {str(e)}") from e
