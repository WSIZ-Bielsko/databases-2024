import os

import asyncpg
from asyncpg import Pool
from dotenv import load_dotenv
from loguru import logger


async def connect_db(database_url: str = None) -> Pool:
    load_dotenv()
    if database_url is None:
        url = os.getenv("DB_URL", None)
        if not url:
            logger.error("DB_URL is not specified.")
            logger.info("Try creating environmental variable or use .env.example.")
            exit(1)
        else:
            logger.warning(f'using DB_URL={url}')
        database_url = url
    pool = await asyncpg.create_pool(database_url, min_size=5, max_size=10, timeout=30, command_timeout=5)
    return pool
