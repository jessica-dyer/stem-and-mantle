from typing import List, Optional

import backoff
from psycopg.errors import InternalError, OperationalError
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from typing_extensions import LiteralString

from config import DATABASE_URL

database_connection_args = {"max_size": 10, "min_size": 0, "open": False, "timeout": 60}
pool = AsyncConnectionPool(conninfo=DATABASE_URL, **database_connection_args)


@backoff.on_exception(backoff.expo, (OperationalError, InternalError), max_tries=5)
async def query_database_many(query: LiteralString, args: Optional[dict]) -> List:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(query, args)
            return await cursor.fetchall()


@backoff.on_exception(backoff.expo, (OperationalError, InternalError), max_tries=5)
async def db_execute_one(query: LiteralString, args: Optional[dict]) -> Optional[dict]:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(query, args)
            return await cursor.fetchone()
