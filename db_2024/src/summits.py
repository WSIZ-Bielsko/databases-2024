import asyncio
import asyncpg
from asyncpg import Pool
from pydantic import BaseModel

"""

create table summit1(
                       id int primary key,
                       name text not null,
                       altitude real default 0,
                       position_long real default 0,
                       position_lat real default 0
);

"""


class Summit(BaseModel):
    id: int
    name: str
    altitude: float
    position_long: float
    position_lat: float


async def connect_db(database_url: str) -> Pool:
    pool = await asyncpg.create_pool(database_url, min_size=5, max_size=10, timeout=30, command_timeout=5)
    return pool


async def get_summits(pool: Pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch('select * from summits')  # here your SQL ...
        for row in rows:
            print(Summit(**row))  # instancje klasy Summit


async def main():
    lonelyMountain = Summit(id=1, name='Lonely Mountain', altitude=441.55, position_long=45.1234, position_lat=67.9854)
    print(lonelyMountain)
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    await get_summits(pool)
    await pool.close()


if __name__ == '__main__':
    asyncio.run(main())  # uruchamia funkcję main ↑↑
