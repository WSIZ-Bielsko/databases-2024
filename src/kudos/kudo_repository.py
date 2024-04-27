import os
from asyncio import run
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from src.kudos.common import connect_db
from src.kudos.model import *

"""
preplexity.ai prompt

Write a class KudoRepository with methods for CRUD operations using asyncpg for the following pydantic data class:

class Kudo(BaseModel):
    id: UUID
    purpose: str  # id_przedmiotu lub inny
    owner_id: str  # album w WD


    
All the method corresponding to Read operation should return instance of Kudo or None.
Assume connection pool is assigned in constructor off KudoRepository
"""


class KudoRepository:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create(self, kudo: Kudo) -> Kudo:
        async with self.pool.acquire() as conn:
            query = """
                  INSERT INTO kudo (id, purpose, owner_id)
                  VALUES ($1, $2, $3)
                  RETURNING *
              """
            row = await conn.fetchrow(query, kudo.id, kudo.purpose, kudo.owner_id)
            return Kudo(**row)

    async def read(self, kudo_id: UUID) -> Kudo | None:
        async with self.pool.acquire() as conn:
            query = """
                SELECT *
                FROM kudo
                WHERE id = $1
            """
            row = await conn.fetchrow(query, kudo_id)
            if row:
                return Kudo(**row)
            else:
                return None

    async def delete(self, kudo_id: UUID) -> None:
        async with self.pool.acquire() as conn:
            query = """
                 DELETE FROM kudo
                 WHERE id = $1
             """
            await conn.execute(query, kudo_id)

    async def update(self, kudo: Kudo) -> Kudo:
        async with self.pool.acquire() as conn:
            query = """
                UPDATE kudo
                SET purpose = $1, owner_id = $2
                WHERE id = $3
                RETURNING *
            """
            row = await conn.fetchrow(query, kudo.purpose, kudo.owner_id, kudo.id)
            return Kudo(**row)

    async def get_kudos_by_personid(self, person_id: str) -> list[Kudo]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM kudo WHERE owner_id = $1"
            records = await connection.fetch(query, person_id)
            return [Kudo(**r) for r in records]

    async def get_kudos_by_purpose_containing(self, keyword: str) -> list[Kudo]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM kudo WHERE purpose LIKE $1"

            # records = await connection.fetch(query, f"%{keyword}%")
            records = await connection.fetch(
                "SELECT * FROM kudo WHERE purpose LIKE '%' || $1 || '%'", keyword
            )
            return [Kudo(**r) for r in records]


async def test_CRD(repo: KudoRepository):
    k1 = Kudo(id=uuid4(), purpose='p1', owner_id='s4411')
    await repo.create(k1)
    logger.info('Create: OK')

    k1_ = await repo.read(k1.id)
    assert k1 == k1_
    logger.info('Read: OK')

    await repo.delete(k1.id)
    k1_deleted = await repo.read(k1.id)
    assert k1_deleted is None
    logger.info('Delete: OK')


async def test_update(repo: KudoRepository):
    # arrange
    k1 = Kudo(id=uuid4(), purpose='p1', owner_id='s4411')
    await repo.create(k1)

    # act
    k1.purpose = 'loremipsum'
    await repo.update(k1)

    # assert
    k1_updated = await repo.read(k1.id)
    assert k1_updated.purpose == k1.purpose
    logger.info('Update: OK')


async def test_get_by_purpose(repo: KudoRepository):
    # arrange
    k1 = Kudo(id=uuid4(), purpose='gg kadabra ss', owner_id='s4411')
    k2 = Kudo(id=uuid4(), purpose='bruh kadabra done', owner_id='s4411')
    await repo.create(k1)
    await repo.create(k2)

    # act
    kudos = await repo.get_kudos_by_purpose_containing('kadabra')

    # assert
    assert len(kudos) >= 2
    print(kudos)



async def main():
    load_dotenv()
    logger.warning('Loading env variables')
    url = os.getenv("DB_URL", None)
    if not url:
        logger.error("DATABASE_URL is not specified.")
        logger.info("Try creating environmental variable or use .env.example.")
        exit(1)
    else:
        logger.warning(f'using DB_URL={url}')

    DATABASE_URL = url
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = KudoRepository(pool=pool)

    await test_CRD(repo)
    # await test_update(repo)
    # await test_get_by_purpose(repo)

if __name__ == '__main__':
    run(main())
