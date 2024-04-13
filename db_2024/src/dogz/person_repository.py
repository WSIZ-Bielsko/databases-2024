import uuid
from asyncio import run
from datetime import datetime, timedelta
from random import randint

import asyncpg
from argon2 import PasswordHasher
from faker import Faker
from loguru import logger

from common import connect_db
from model import *

"""
preplexity.ai prompt

Write a class PersonCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class Person(BaseModel):
    id: UUID 
    pesel: str
    name: str
    phone: str
    password_hash: str

"""


class PersonCRUD:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create(self, person: Person) -> Person:
        query = """
            INSERT INTO persons (id, pesel, name, phone, password_hash)
            VALUES ($1, $2, $3, $4, $5)
        """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                person.id,
                person.pesel,
                person.name,
                person.phone,
                person.password_hash
            )

    async def read(self, person_id: UUID) -> Person | None:
        query = """
        SELECT *
        FROM persons
        WHERE id = $1
        """
        row = await self.pool.fetchrow(query, person_id)
        if row is None: return None

        return Person(**row)

    async def read_all(self) -> list[Person]:
        query = """
        SELECT *
        FROM persons
        """
        rows = await self.pool.fetch(query)
        return [Person(**row) for row in rows]

    async def update(self, person: Person):
        query = """
                   UPDATE persons
                   SET pesel = $1, name = $2, phone = $3, password_hash = $4
                   WHERE id = $5
               """

        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                person.pesel,
                person.name,
                person.phone,
                person.password_hash,
                person.id
            )

    async def delete(self, person_id: UUID):
        query = """
            DELETE FROM persons
            WHERE id = $1
            """
        await self.pool.execute(query, person_id)

    # --- extra methods


def random_person():
    faker = Faker()
    ph = PasswordHasher()
    return Person(
        id=uuid.uuid4(),
        pesel=faker.ssn(),
        name=faker.name(),
        phone=faker.phone_number(),
        password_hash=ph.hash('1234')
    )


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = PersonCRUD(pool=pool)
    logger.info('connection works')
    p = random_person()
    await repo.create(person=p)
    print(p)

    p2 = await repo.read(person_id=p.id)
    assert p == p2

    await repo.delete(person_id=p.id)
    p_none = await repo.read(person_id=p.id)
    assert p_none is None

    all_persons = await repo.read_all()
    print(all_persons)

if __name__ == '__main__':
    run(main())
