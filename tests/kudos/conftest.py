import os
from uuid import uuid4

import pytest_asyncio
from dotenv import load_dotenv
from loguru import logger

from src.kudos.common import connect_db
from src.kudos.kudo_repository import KudoRepository
from src.kudos.model import Kudo


@pytest_asyncio.fixture
async def kudoRepo():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL", None)
    logger.warning(f'using database: {db_url}')

    if not db_url:
        logger.error("[-] DATABASE_URL is not specified.")
        exit(1)
    pool = await connect_db(db_url)
    logger.warning('db connection successful')
    kudoRepo = KudoRepository(pool)
    return kudoRepo


@pytest_asyncio.fixture
async def kudo1(kudoRepo: KudoRepository):
    kudo = Kudo(id=uuid4(), purpose='testing', owner_id='s4444')
    existing = await kudoRepo.read(kudo.id)
    if existing is None:
        logger.info(f'creating kudo with id={kudo.id}')
        await kudoRepo.create(kudo)
    yield kudo
    await kudoRepo.delete(kudo.id)
    logger.info(f'removing kudo with id={kudo.id}')


@pytest_asyncio.fixture
async def kudo2(kudoRepo: KudoRepository):
    kudo = Kudo(id=uuid4(), purpose='testing', owner_id='s4444')
    existing = await kudoRepo.read(kudo.id)
    if existing is None:
        logger.info(f'creating kudo with id={kudo.id}')
        await kudoRepo.create(kudo)
    yield kudo
    await kudoRepo.delete(kudo.id)
    logger.info(f'removing kudo with id={kudo.id}')
