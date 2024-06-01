import datetime
import os

import asyncpg
from asyncpg import Pool
from dotenv import load_dotenv
from loguru import logger


async def connect_db() -> Pool:
    load_dotenv()
    logger.info("Loading env variables")
    url = os.getenv("DB_URL", None)

    pool = await asyncpg.create_pool(
        url, min_size=5, max_size=10, timeout=30, command_timeout=5
    )
    return pool



def ts():
    return datetime.datetime.now().timestamp()
