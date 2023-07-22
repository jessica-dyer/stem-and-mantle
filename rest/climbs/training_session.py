from datetime import date
from typing import Optional

import asyncpg
from fastapi import Depends, HTTPException
from pydantic import BaseModel


class TrainingSession(BaseModel):
    user_id: int
    date: date
    notes: Optional[str]


async def create_training_session(training_session: TrainingSession, db: asyncpg.Pool = Depends()):
    query = """
        INSERT INTO training_sessions (user_id, date, notes)
        VALUES ($1, $2, $3)
        RETURNING id, user_id, date, notes
    """
    try:
        result = await db.fetchrow(
            query,
            training_session.user_id,
            training_session.date,
            training_session.notes,
        )
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
