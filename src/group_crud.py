import os
from asyncio import run

from src.db_service import DbService
from model import Group

DEFAULT_DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
DATABASE_URL = os.getenv('DB_URL', DEFAULT_DATABASE_URL)

"""
perplexity.ai prompt:

write a class GroupCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class Group(BaseModel):
    grupaid: int
    nazwa: str
    opis: str
    active: bool
    
in each method get the connection via `async with self.pool.acquire() as conn:`. 
    


"""

class GroupCRUD:
    def __init__(self, pool):
        self.pool = pool

    async def create_group(self, group: Group):
        async with self.pool.acquire() as conn:
            query = "INSERT INTO groups (grupaid, nazwa, opis, active) VALUES ($1, $2, $3, $4) RETURNING grupaid"
            record = await conn.fetchrow(query, group.grupaid, group.nazwa, group.opis, group.active)
            return record['grupaid']

    async def read_group(self, grupaid: int):
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM groups WHERE grupaid = $1"
            record = await conn.fetchrow(query, grupaid)
            if record:
                return Group(**record)

    async def update_group(self, group: Group):
        async with self.pool.acquire() as conn:
            query = "UPDATE groups SET nazwa = $2, opis = $3, active = $4 WHERE grupaid = $1"
            await conn.execute(query, group.grupaid, group.nazwa, group.opis, group.active)

    async def delete_group(self, grupaid: int):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM groups WHERE grupaid = $1"
            await conn.execute(query, grupaid)


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()

    pool = db.pool
    repo = GroupCRUD(pool)
    group = Group(grupaid=991, nazwa='Zielarze', opis='N/A', active=True)
    await repo.create_group(group)

    g = await repo.read_group(grupaid=991)
    print(g)
    z = await repo.delete_group(grupaid=991)
    print(z)  # None
    g = await repo.read_group(grupaid=991)
    print(g)  # None


if __name__ == '__main__':
    # print(DATABASE_URL)
    run(main())
