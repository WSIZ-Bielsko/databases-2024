import os
import secrets
from asyncio import run, create_task, gather, sleep
from uuid import UUID, uuid4

import asyncpg
from argon2 import PasswordHasher
from asyncpg import Pool
from dotenv import load_dotenv
from loguru import logger

from src.corporate_vote.model import User, Results

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

    async def create_new_vote(self) -> Results:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                INSERT INTO results (yes_count, no_count, pass_count)
                VALUES ($1, $2, $3)
                RETURNING *
                """,
                0, 0, 0
            )
            return Results(**result) if result else None

    async def get_results(self, vote_id: int) -> Results | None:
        logger.info(f'Getting results of vote id={vote_id}')
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT * FROM results WHERE vote_id = $1",
                vote_id
            )
            return Results(**result) if result else None

    async def reset_results(self, vote_id: int):
        logger.info(f'Resetting results of vote id={vote_id}')
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE results set yes_count=0, no_count=0, pass_count=0 where"
                " vote_id = $1",
                vote_id
            )
            await conn.execute("DELETE FROM participation where vote_id = $1", vote_id)

    async def has_participated(self, email: str, vote_id: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT EXISTS(
                    SELECT 1 FROM participation WHERE email = $1 AND vote_id = $2
                )
                """,
                email, vote_id
            )
            return result[0]

    # ----------- custom methods

    async def login(self, email: str, password: str) -> str | None:
        """

        :param email:
        :param password: (will be hashed)
        :return: token
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction(isolation='repeatable_read'):
                # {'serializable', 'repeatable_read', 'read_uncommitted', 'read_committed'}
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

    async def get_user_by_token(self, token: str) -> User | None:
        """

        :param token:
        :return: User who has user.token == token
        """
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM users WHERE token = $1"
            row = await self.pool.fetchrow(query, token)
            if row is None:
                return None
            else:
                return User(**row)

    async def vote(self, token: str, vote_type: str, vote_id: int):

        if vote_type not in ['yes', 'no', 'pass']:
            raise RuntimeError('Vote type must be "yes" or "no" or "pass"')
        await sleep(0.05)

        # todo: transactional
        #    1. get user with given token
        #    2. check if email already participated
        #    3. update results with shares of user
        #    4. update participation for email

        # todo: add parameter "request_id"; catch asyncpg.exceptions.SerializationError

        async with self.pool.acquire() as conn:
            async with conn.transaction(isolation='serializable'):
                # {'serializable', 'repeatable_read', 'read_uncommitted', 'read_committed'}

                logger.info(f'token {token} inside transaction')
                query_read_user = 'SELECT * FROM users WHERE token = $1'

                query_read_participation = ('SELECT COUNT(*) FROM participation '
                                            'WHERE vote_id = $1 and email = $2')

                query_update_results = (f'UPDATE results SET '
                                        f'{vote_type}_count = {vote_type}_count + $1 '
                                        f'where vote_id = $2')

                query_update_particiaption = 'INSERT INTO participation (vote_id, email) values ($1, $2)'

                # 1 Read user
                result = await conn.fetchrow(query_read_user, token)
                if not result:
                    raise RuntimeError('Invalid token')
                user = User(**result)

                # 2 Read participation
                participation_count = await conn.fetchval(query_read_participation, vote_id, user.email)
                if participation_count > 0:
                    raise RuntimeError('User has already participated in the vote')
                logger.info(f'Token {token} ready to vote')

                # 3 Update results
                await conn.execute(query_update_results, user.shares, vote_id)
                logger.info(f'Token {token} result updated')

                # 4 Update participation
                await conn.execute(query_update_particiaption, vote_id, user.email)
                logger.info(f'Token {token} participation marked')

            logger.info('transaction finished')

    """
    Challenges: 
    - do steps 1,2, then pause... redo 1-4 for other call; resume with 3,4
    
    """


async def hack_vote(db: DbRepository, token: str, vote_id: int):
    await sleep(0.1)
    await db.vote(token, 'no', vote_id)


async def main():
    pool = await connect_db()
    db = DbRepository(pool)
    # vote = await db.create_new_vote()
    # u = User(id=uuid4(), email='a@a.com', password='kadabra', token='---', shares=1,
    #          active=True)
    # await db.create_user(u)

    tkn = await db.login('a@a.com', 'kadabra')

    # u = await db.get_user_by_token(tkn)
    # print(u)
    # assert u.email == 'a@a.com'

    await db.reset_results(vote_id=3)

    try:
        tasks = []
        for i in range(40):
            tasks.append(create_task(hack_vote(db, tkn, vote_id=3)))

        await gather(*tasks)
    except Exception as e:
        logger.error(e)

    result = await db.get_results(vote_id=3)
    logger.debug('Done: ' + str([r.done() for r in tasks]))
    logger.debug('Cancelled: ' + str([r.cancelled() for r in tasks]))
    logger.warning('Final results')
    logger.warning(result)

    await pool.close()


if __name__ == '__main__':
    run(main())
