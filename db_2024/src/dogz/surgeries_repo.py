from asyncio import run
from uuid import UUID, uuid4

import asyncpg

from common import connect_db
from model import *


class SurgeriesRepo:

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create_surgery(self, surgery: Surgery):
        s = surgery
        async with self.pool.acquire() as connection:
            query = """INSERT INTO surgeries (id, dog_id, date_performed, description) 
                        VALUES ($1, $2, $3, $4) RETURNING *"""
            record = await connection.fetchrow(query, s.id, s.dog_id, s.date_performed, s.description)
            return

    async def get_surgery(self, surgery_id: UUID) -> Surgery | None:
        pass

    async def update_surgery(self, surgery: Surgery):
        pass

    async def delete_surgery(self, surgery_id: UUID):
        pass


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = SurgeriesRepo(pool=pool)

    surgery = Surgery(id=uuid4(), dog_id=UUID('e943f5f5-1225-4187-967d-375849c17ba3'),
                      date_performed=datetime.now(), description='little cut...')

    await repo.create_surgery(surgery)

if __name__ == '__main__':
    run(main())
