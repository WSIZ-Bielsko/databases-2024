import os
from asyncio import run
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from src.kudos.common import connect_db
from src.kudos.model import Kudo, User
from uuid import UUID

"""
preplexity.ai prompt

Write a class UserRepository with methods for CRUD operations using asyncpg
for the following pydantic data class:

class User(BaseModel):
    id: str
    name: str

All the method corresponding to Read operation should return instance of
User or None.
Assume connection pool is assigned in constructor off KudoRepository
"""


class KudoRepository:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO users (id, name) VALUES ($1, $2)",
                    user.id, user.name
                )
        return user

    async def read(self, user_id: str) -> User | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            if row:
                return User(**dict(row))
            return None

    async def delete(self, user_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM users WHERE id = $1",
                user_id
            )

    async def update(self, user: User):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET name = $1 WHERE id = $2",
                user.name, user.id
            )
