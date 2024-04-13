from asyncio import run
from uuid import UUID, uuid4

import asyncpg
from loguru import logger

from common import connect_db
from model import *


class SurgeriesRepo:

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create_surgery(self, surgery: Surgery):
        """
        AI prompt:
        Write a method `async def create_surgery(self, surgery: Surgery):` for a class {...}
        using asyncpg; the class contains a field pool: asyncpg.pool.Pool

        :param surgery:
        :return:
        """
        s = surgery
        async with self.pool.acquire() as connection:
            query = """INSERT INTO surgeries (id, dog_id, date_performed, description) 
                        VALUES ($1, $2, $3, $4)"""
            await connection.execute(query, s.id, s.dog_id, s.date_performed, s.description)

    async def get_surgery(self, surgery_id: UUID) -> Surgery | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from surgeries where id=$1', surgery_id)
            if row is None:
                return None
            return Surgery(**row)

    async def update_surgery(self, surgery: Surgery):
        """
            AI Prompt:
            Write a method `async def update_surgery(self, surgery: Surgery):` for a class {...}
            using asyncpg; the class contains a field pool: asyncpg.pool.Pool


            Updates an existing surgery in the database.

            Args:
                surgery (Surgery): The surgery object to be updated.

            Returns:
                None
            """
        query = """
                UPDATE surgeries
                SET dog_id = $1, date_performed = $2, description = $3
                WHERE id = $4
            """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                surgery.dog_id,
                surgery.date_performed,
                surgery.description,
                surgery.id
            )

    async def delete_surgery(self, surgery_id: UUID):
        async with self.pool.acquire() as connection:
            await connection.execute("delete from surgeries where id=$1", surgery_id)
            logger.info(f'removed surgery with id={surgery_id}')

async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = SurgeriesRepo(pool=pool)

    surgery = Surgery(id=uuid4(), dog_id=UUID('e943f5f5-1225-4187-967d-375849c17ba3'),
                      date_performed=datetime.now(), description='little cut...')

    await repo.create_surgery(surgery)
    sid = surgery.id
    surgery_ = await repo.get_surgery(sid)
    print(surgery_)
    surgery.description = 'some uneven cuts...'
    await repo.update_surgery(surgery)
    surgery3 = await repo.get_surgery(sid)
    print(surgery3)
    await repo.delete_surgery(sid)



if __name__ == '__main__':
    run(main())
