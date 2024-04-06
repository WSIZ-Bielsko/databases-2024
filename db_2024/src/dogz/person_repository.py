import uuid
from asyncio import run
from datetime import datetime, timedelta
from random import randint

import asyncpg
from faker import Faker
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
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create(self, person: Person) -> Person:
        query = """
        INSERT INTO persons (pesel, name, phone)
        VALUES ($1, $2, $3)
        RETURNING id, pesel, name, phone
        """
        row = await self.pool.fetchrow(query, person.pesel, person.name, person.phone)
        return Person(id=row['id'], pesel=row['pesel'], name=row['name'], phone=row['phone'])

    async def read(self, person_id: UUID) -> Person | None:
        query = """
        SELECT id, pesel, name, phone
        FROM persons
        WHERE id = $1
        """
        row = await self.pool.fetchrow(query, person_id)
        if row is None: return None

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


def random_person():
    faker = Faker()
    return Person(
        id=uuid.uuid4(),
        pesel=faker.ssn(),
        name=faker.name(),
        phone=faker.phone_number()
    )


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = PersonCRUD(pool=pool)
    logger.info('connection works')
    p = random_person()
    p_created = await repo.create(person=p)
    p.id = p_created.id
    print(p)
    print(p_created)
    assert p == p_created

    p2 = await repo.read(person_id=p.id)
    assert p == p2

    await repo.delete(person_id=p.id)
    p_none = await repo.read(person_id=p.id)
    assert p_none is None


if __name__ == '__main__':
    run(main())
