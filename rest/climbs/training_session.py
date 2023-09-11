from datetime import date
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from rest.database import db_execute_one, query_database_many


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


async def get_training_sessions(user_id: int):
    query = """
    SELECT * FROM training_sessions where user_id = %(user_id)s;
    """
    args = {"user_id": user_id}
    training_sessions = await query_database_many(query=query, args=args)
    if training_sessions:
        data = [
            {"id": session["id"], "date": session["date"], "notes": session["notes"]} for session in training_sessions
        ]
    else:
        data = []
    return {"training_sessions": data}
