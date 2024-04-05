import uuid
from asyncio import run
from datetime import datetime, timedelta

import asyncpg
from loguru import logger

from common import connect_db
from model import *

"""
preplexity.ai prompt

Write a class PersonCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class Person(BaseModel):
    id: UUID | None
    pesel: str
    name: str
    phone: str

    
    
All the method corresponding to Read operation should return instance of the relevant dataclass.
The method corresponding to Create operation should return instance of created dataclass.

"""


class PersonCRUD:
    def __init__(self, pool: asyncpg.Connection):
        self.pool = pool

    async def create(self, person: Person) -> Person:
        query = """
        INSERT INTO persons (pesel, name, phone)
        VALUES ($1, $2, $3)
        RETURNING id, pesel, name, phone
        """
        row = await self.pool.fetchrow(query, person.pesel, person.name, person.phone)
        return Person(id=row['id'], pesel=row['pesel'], name=row['name'], phone=row['phone'])

    async def read(self, person_id: UUID) -> Person:
        query = """
        SELECT id, pesel, name, phone
        FROM persons
        WHERE id = $1
        """
        row = await self.pool.fetchrow(query, person_id)
        return Person(id=row['id'], pesel=row['pesel'], name=row['name'], phone=row['phone'])

    async def read_all(self) -> list[Person]:
        query = """
        SELECT id, pesel, name, phone
        FROM persons
        """
        rows = await self.pool.fetch(query)
        return [Person(id=row['id'], pesel=row['pesel'], name=row['name'], phone=row['phone']) for row in rows]

    async def update(self, person: Person) -> Person:
        query = """
        UPDATE persons
        SET pesel = $1, name = $2, phone = $3
        WHERE id = $4
        RETURNING id, pesel, name, phone
        """
        row = await self.pool.fetchrow(query, person.pesel, person.name, person.phone, person.id)
        return Person(id=row['id'], pesel=row['pesel'], name=row['name'], phone=row['phone'])

    async def delete(self, person_id: UUID) -> None:
        query = """
        DELETE FROM persons
        WHERE id = $1
        """
        await self.pool.execute(query, person_id)

    # --- extra methods


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = PersonCRUD(pool=pool)

    # dd = await repo.get_dogs_older_than(age_mths=10, limit=10, offset=0)
    # dd = await repo.get_dogs_name_containing(substring_of_name='ya', limit=10, offset=0)
    # for d in dd:
    #     print(d.birthdate, d.name, d.lineage, d.id)


if __name__ == '__main__':
    run(main())
