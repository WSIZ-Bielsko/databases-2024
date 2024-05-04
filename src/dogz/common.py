import asyncpg
from asyncpg import Pool


async def connect_db(database_url: str) -> Pool:
    pool = await asyncpg.create_pool(
        database_url, min_size=5, max_size=10, timeout=30, command_timeout=5
    )
    return pool
