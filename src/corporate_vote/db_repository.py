import os
import secrets
from asyncio import run
from uuid import UUID, uuid4

import asyncpg
from argon2 import PasswordHasher
from asyncpg import Pool
from dotenv import load_dotenv
from loguru import logger

from src.corporate_vote.model import User

"""
preplexity.ai prompt

Write a class EntityRepository with methods for CRUD operations using asyncpg
for the following pydantic data class:


class User(BaseModel):
    id: UUID
    email: str
    password: str
    token: str
    shares: int
    active: bool

Apart from the method corresponding to delete operation, all other ms should return 
instance or instances of the dataclass or None.

Assume connection pool is assigned in constructor of EntityRepository.

In the result, replace "Optional" by " | None" python construct.  

Create instances of the dataclass by (**result) code. 

Use `select *` in list and get methods. 

Use modern python syntax (python >= 3.11), don't use the typing package. 

In update method use "returning *" in sql. 

Use plural for table name in sql. 

The methods should have a suffix equal to the dataclass name. 
"""


async def connect_db() -> Pool:
    load_dotenv()
    logger.info("Loading env variables")
    url = os.getenv("DB_URL", None)

    pool = await asyncpg.create_pool(
        url, min_size=5, max_size=10, timeout=30, command_timeout=5
    )
    return pool


class DbRepository:

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create_user(self, user: User) -> User | None:

        ph = PasswordHasher()
        user.password = ph.hash(user.password)

        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO users (id, email, password, token, shares, active, is_admin)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """,
                user.id, user.email, user.password, user.token,
                user.shares, user.active, user.is_admin
            )
            return User(**result) if result else None

    async def get_user(self, user_id: UUID) -> User | None:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            return User(**result) if result else None

    async def list_users(self) -> list[User]:
        async with self.pool.acquire() as conn:
            results = await conn.fetch("SELECT * FROM users")
            return [User(**result) for result in results]

    async def update_user(self, user: User) -> User | None:
        ph = PasswordHasher()
        user.password = ph.hash(user.password)
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                UPDATE users
                SET email = $2, password = $3, token = $4, shares = $5, active = $6, 
                    is_admin = $7
                WHERE id = $1
                RETURNING *
                """,
                user.id, user.email, user.password, user.token, user.shares,
                user.active, user.is_admin
            )
            return User(**result) if result else None

    async def delete_user(self, user_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE id = $1",
                user_id
            )
            return result == "DELETE 1"

    # ----------- custom methods

    async def login(self, email: str, password: str) -> str | None:
        """

        :param email:
        :param password: (will be hashed)
        :return: token
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Fetch user data
                query = "SELECT * FROM users WHERE email = $1"
                row = await conn.fetchrow(query, email)

                if not row:
                    return None

                ph = PasswordHasher()
                ph.verify(row['password'], password)  # raises error on mismatch

                new_token = secrets.token_urlsafe(32)

                # Update user with new token
                update_query = """
                    UPDATE users users
                    SET token = $1 
                    WHERE id = $2
                    """
                await conn.execute(update_query, new_token, row['id'])

                return new_token

    async def vote(self, token: str, vote_type: str):
        if vote_type not in ['yes', 'no', 'pass']:
            raise RuntimeError('Vote type must be "yes" or "no" or "pass"')
        # todo: transactional
        #    1. get user with given token
        #    2. check if email already participated
        #    3. update results with shares of user
        #    4. update participation for email

    """
    Challenges: 
    - do steps 1,2, then pause... redo 1-4 for other call; resume with 3,4
    
    """


async def main():
    pool = await connect_db()
    db = DbRepository(pool)
    # u = User(id=uuid4(), email='a@a.com', password='kadabra', token='---', shares=1,
    #          active=True)
    # await db.create_user(u)

    tkn = await db.login('a@a.com', 'kadabra')

    print(tkn)

    await pool.close()


if __name__ == '__main__':
    run(main())
