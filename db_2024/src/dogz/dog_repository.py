import uuid
from asyncio import run
from datetime import datetime, timedelta
from random import choice

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

    async def read_all(self) -> list[Dog]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM dogs"
            record = await connection.fetch(query)
            return [Dog(**r) for r in record]

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

    async def get_dogs_older_than(self, age_mths: int, limit: int, offset: int) -> list[Dog]:
        bdate = datetime.now() - timedelta(days=30 * age_mths)
        async with self.pool.acquire() as connection:
            query = "SELECT * from dogs where birthdate > $1 order by birthdate asc, id limit $2 offset $3"
            records = await connection.fetch(query, bdate, limit, offset)
            return [Dog(**record) for record in records]

    async def get_dogs_name_containing(self, substring_of_name: str, limit: int, offset: int) -> list[Dog]:
        async with self.pool.acquire() as connection:
            pattern = f'%{substring_of_name}%'
            query = "select * from dogs where name ilike $1 order by name limit $2 offset $3"
            records = await connection.fetch(query, pattern, limit, offset)
            return [Dog(**record) for record in records]

    async def get_persons_assigned_to_dog(self, dog_id: UUID) -> list[Person]:
        async with self.pool.acquire() as connection:
            query = "select p.id, pesel, name, phone from persons p, person_dogs pd where p.id = pd.person_id and pd.dog_id = $1;"
            records = await connection.fetch(query, dog_id)
            return [Person(**record) for record in records]

    async def assign_person_to_dog(self, person_id: UUID, dog_id: UUID):
        async with self.pool.acquire() as connection:
            try:
                query = "insert into person_dogs(dog_id, person_id) values ($1,$2)"
                records = await connection.execute(query, dog_id, person_id)
            except asyncpg.exceptions.UniqueViolationError:
                logger.warning(f'Dog {dog_id=} already assigned to person {person_id=}')

    async def get_dogs_assigned_to_person(self, person_id: UUID) -> list[Dog]:
        async with self.pool.acquire() as connection:
            # todo: avoid listing all columns
            query = """select dogs.id, dogs.breed_id, dogs.lineage, dogs.birthdate, dogs.name from dogs, person_dogs where 
                       person_dogs.person_id = $1 and person_dogs.dog_id = dogs.id;"""
            records = await connection.fetch(query, person_id)
            return [Dog(**record) for record in records]


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = DogsCRUD(pool=pool)

    # dd = await repo.get_dogs_older_than(age_mths=10, limit=10, offset=0)
    # dd = await repo.get_dogs_name_containing(substring_of_name='ya', limit=10, offset=0)
    # for d in dd:
    #     print(d.birthdate, d.name, d.lineage, d.id)

    # d = Dog(id=uuid.uuid4(), breed_id=uuid.uuid4(), lineage='LinKat', birthdate=date(2020, 1, 15), name='Szarik')
    # logger.info(d)
    # d = await repo.create_dog(d)
    # logger.info('dog zapisany')
    #
    # found_dog = await repo.read_dog(dog_id=d.id)
    # # print(type(found_dog))  # <class 'asyncpg.Record'>
    # logger.info(found_dog)
    # logger.info(type(found_dog))  # type = Dog
    # logger.info(found_dog == d)
    #
    # found_dog.lineage = 'Extinct'
    # await repo.update_dog(d.id, found_dog)
    #
    # zz = await repo.read_dog(d.id)
    # logger.info(zz)

    # await repo.delete_dog(d.id)
    #
    # deleted_dog = await repo.read_dog(d.id)
    # logger.warning(deleted_dog)  # None

    await repo.assign_person_to_dog(person_id=UUID('00000000-9076-4798-95e2-aaababaad92f'),
                                    dog_id=UUID('0667c52b-fb32-487c-aebf-aaad435334b9'))

    # owners = await repo.get_persons_assigned_to_dog(dog_id=UUID('0667c52b-fb32-487c-aebf-811d435334b9'))

    # my_dogs = await repo.get_dogs_assigned_to_person(person_id=UUID('e75b3ff3-9106-4bca-8b1c-9a7ec716a943'))
    # for d in my_dogs:
    #     print(d)


if __name__ == '__main__':
    run(main())
