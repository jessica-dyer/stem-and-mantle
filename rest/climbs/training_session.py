from datetime import date
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from rest.database import db_execute_one


class TrainingSession(BaseModel):
    date: date
    notes: Optional[str]


async def create_training_session(user_id: int, training_session: TrainingSession):
    query = """
        INSERT INTO training_sessions (user_id, date, notes)
        VALUES (%(user_id)s, %(date)s, %(notes)s)
        RETURNING id, user_id, date, notes
    """
    try:
        args = {"user_id": user_id, "date": training_session.date, "notes": training_session.notes}
        result = await db_execute_one(query=query, args=args)
        if result:
            return {
                "training_session": {
                    "id": result["id"],
                    "user_id": result["user_id"],
                    "date": result["date"],
                    "notes": result["notes"],
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating training session: {str(e)}") from e
