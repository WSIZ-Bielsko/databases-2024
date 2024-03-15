from asyncio import run
from datetime import date

import asyncpg
from asyncpg import Pool
from pydantic import BaseModel


class Dog(BaseModel):
    id: int | None
    breed_id: int
    lineage: str
    birthdate: date
    name: str


async def connect_db(database_url: str) -> Pool:
    pool = await asyncpg.create_pool(database_url, min_size=5, max_size=10, timeout=30, command_timeout=5)
    return pool


"""
preplexity.ai prompt

write a class DogsCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class Dog(BaseModel):
    id: int | None
    breed_id: int
    lineage: str
    birthdate: date
    name: str
    
in each method get the connection via `async with self.pool.acquire() as conn:`. In the create method assume 
the database will generate the id value; the create_dog method should return full Dog. 



"""


class DogsCRUD:
    def __init__(self, pool: Pool):
        self.pool: Pool = pool

    async def create_dog(self, dog: Dog) -> Dog:
        async with self.pool.acquire() as conn:
            query = "INSERT INTO dogs (breed_id, lineage, birthdate, name) VALUES ($1, $2, $3, $4) RETURNING id"
            id = await conn.fetchval(query, dog.breed_id, dog.lineage, dog.birthdate, dog.name)
            dog.id = id
            return dog

    async def get_dog(self, dog_id: int):
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM dogs WHERE id = $1"
            dog = await conn.fetchrow(query, dog_id)
            return dog

    async def update_dog(self, dog_id: int, dog: Dog):
        async with self.pool.acquire() as conn:
            query = "UPDATE dogs SET breed_id = $1, lineage = $2, birthdate = $3, name = $4 WHERE id = $5"
            await conn.execute(query, dog.breed_id, dog.lineage, dog.birthdate, dog.name, dog_id)

    async def delete_dog(self, dog_id: int):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM dogs WHERE id = $1"
            await conn.execute(query, dog_id)


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = DogsCRUD(pool=pool)

    d = Dog(id=None, breed_id=117, lineage='LinKat', birthdate=date(2020, 1, 15), name='Szarik')
    print(d)
    created_dog = await repo.create_dog(d)
    print('dog zapisany; dostalismy:', created_dog)



if __name__ == '__main__':
    run(main())
