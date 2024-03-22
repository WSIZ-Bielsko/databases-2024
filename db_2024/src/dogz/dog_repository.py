import uuid
from asyncio import run

import asyncpg
from loguru import logger

from common import connect_db
from model import *

"""
preplexity.ai prompt
create a table on postgres 15 database that would correspond to the following pydantic class

class Dog(BaseModel):
    id: UUID | None
    breed_id: UUID
    lineage: str
    birthdate: date
    name: str
    
For `str` fields use `text` type.
The `id` field should be generated per default.

"""

"""
preplexity.ai prompt

Write a class DogsCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class Dog(BaseModel):
    id: UUID | None
    breed_id: UUID
    lineage: str
    birthdate: date
    name: str
    dominant_color: str

    
All the method corresponding to Read operation should return instance of Dog or None.
The method corresponding to Create operation should return instance of created Dog.
"""


class DogsCRUD:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create_dog(self, dog: Dog) -> Dog:
        async with self.pool.acquire() as connection:
            query = "INSERT INTO dogs (id, breed_id, lineage, birthdate, name) VALUES ($1, $2, $3, $4, $5) RETURNING *"
            record = await connection.fetchrow(query, dog.id, dog.breed_id, dog.lineage, dog.birthdate, dog.name)
            return Dog(**record)

    async def read_dog(self, dog_id: uuid.UUID) -> Dog | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM dogs WHERE id = $1"
            record = await connection.fetchrow(query, dog_id)
            return Dog(**record) if record else None

    async def update_dog(self, dog_id: uuid.UUID, dog: Dog) -> None:
        async with self.pool.acquire() as connection:
            query = "UPDATE dogs SET breed_id = $1, lineage = $2, birthdate = $3, name = $4 WHERE id = $5"
            await connection.execute(query, dog.breed_id, dog.lineage, dog.birthdate, dog.name, dog_id)

    async def delete_dog(self, dog_id: uuid.UUID) -> None:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM dogs WHERE id = $1"
            await connection.execute(query, dog_id)

    # --- extra methods

    # AI: Write a method (using self.pool) to remove all instances from the db where lineage is "Extinct"
    async def remove_extinct_dogs(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM dogs WHERE lineage = 'Extinct'")

    # AI: Write a method (using self.pool) returning all instances of Dog from the db where lineage has a value given in the argument of the method

    async def get_dogs_by_lineage(self, lineage: str) -> list[Dog]:
        async with self.pool.acquire() as connection:
            query = "SELECT id, breed_id, lineage, birthdate, name FROM dogs WHERE lineage = $1"
            records = await connection.fetch(query, lineage)
            return [Dog(**record) for record in records]


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = DogsCRUD(pool=pool)

    d = Dog(id=uuid.uuid4(), breed_id=uuid.uuid4(), lineage='LinKat', birthdate=date(2020, 1, 15), name='Szarik')
    logger.info(d)
    d = await repo.create_dog(d)
    logger.info('dog zapisany')

    found_dog = await repo.read_dog(dog_id=d.id)
    # print(type(found_dog))  # <class 'asyncpg.Record'>
    logger.info(found_dog)
    logger.info(type(found_dog))  # type = Dog
    logger.info(found_dog == d)

    found_dog.lineage = 'Extinct'
    await repo.update_dog(d.id, found_dog)

    zz = await repo.read_dog(d.id)
    logger.info(zz)

    # await repo.delete_dog(d.id)
    #
    # deleted_dog = await repo.read_dog(d.id)
    # logger.warning(deleted_dog)  # None


if __name__ == '__main__':
    run(main())
