from loguru import logger

from src.remote_tasks.model import JobRequest, User

"""
preplexity.ai prompt

Write a class KudoRepository with methods for CRUD operations using asyncpg
for the following pydantic data class:

class Kudo(BaseModel):
    id: UUID
    purpose: str  # id_przedmiotu lub inny
    owner_id: str  # album w WD

All the method corresponding to Read operation should return instance of
Kudo or None.
Assume connection pool is assigned in constructor off KudoRepository
"""
import asyncpg
from typing import Optional
from uuid import UUID


class TaskCrudRepository:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    # requests

    async def create_task(self, job_request: JobRequest) -> JobRequest:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    INSERT INTO "JobRequest" (
                        id, repo_url, commit, image_tag, entry_point_file,
                        env_file_content, cpu, ram_mb, priority, user_id, submitted_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    RETURNING *
                    """,
                    job_request.id, job_request.repo_url, job_request.commit, job_request.image_tag,
                    job_request.entry_point_file, job_request.env_file_content, job_request.cpu,
                    job_request.ram_mb, job_request.priority, job_request.user_id, job_request.submitted_at
                )
                return JobRequest(**row)

    async def create_multiple_task(self, job_reqs: list[JobRequest]):
        async with self.pool.acquire() as conn:
            logger.info(f'Creating {len(job_reqs)}')
            query = """
                INSERT INTO JobRequest (
                    id, repo_url, commit, image_tag, entry_point_file,
                    env_file_content, cpu, ram_mb, priority, user_id, submitted_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """
            data = [(
                r.id, r.repo_url, r.commit, r.image_tag, r.entry_point_file,
                r.env_file_content, r.cpu, r.ram_mb, r.priority, r.user_id,
                r.submitted_at
            ) for r in job_reqs]

            await conn.executemany(query, data)
            logger.info(f'Creating {len(job_reqs)} requests complete')

    async def read_task(self, job_request_id: UUID) -> JobRequest | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM "JobRequest" WHERE id = $1
                """,
                job_request_id
            )
            if row:
                return JobRequest(**row)
            return None

    async def read_all_tasks(self) -> list[JobRequest]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM "JobRequest"
                """
            )
            return [JobRequest.parse_obj(row) for row in rows]

    async def update_task(self, job_request: JobRequest) -> Optional[JobRequest]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    UPDATE JobRequest
                    SET repo_url = $2, commit = $3, image_tag = $4, entry_point_file = $5,
                        env_file_content = $6, cpu = $7, ram_mb = $8, priority = $9,
                        user_id = $10, submitted_at = $11
                    WHERE id = $1
                    RETURNING *
                    """,
                    job_request.id, job_request.repo_url, job_request.commit, job_request.image_tag,
                    job_request.entry_point_file, job_request.env_file_content, job_request.cpu,
                    job_request.ram_mb, job_request.priority, job_request.user_id, job_request.submitted_at
                )
                if row:
                    return JobRequest.parse_obj(row)
                return None

    async def delete_task(self, job_request_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    DELETE FROM "JobRequest"
                    WHERE id = $1
                    RETURNING *
                    """,
                    job_request_id
                )
                return bool(row)

    # users

    async def create_user(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    INSERT INTO "users" (id, name)
                    VALUES ($1, $2)
                    RETURNING *
                    """,
                    user.id, user.name
                )
                u = User(**row)
                logger.info(f'Created user {u}')
                return u

    async def read_user(self, user_id: UUID) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM "users" WHERE id = $1
                """,
                user_id
            )
            if row:
                return User.parse_obj(row)
            return None

    async def read_all_users(self) -> list[User]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM "users"
                """
            )
            return [User(**row) for row in rows]

    async def update_user(self, user: User) -> User | None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    UPDATE "users"
                    SET name = $2
                    WHERE id = $1
                    RETURNING *
                    """,
                    user.id, user.name
                )
                if row:
                    return User.parse_obj(row)
                return None

    async def delete_user(self, user_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    DELETE FROM "users"
                    WHERE id = $1
                    RETURNING *
                    """,
                    user_id
                )
                return bool(row)
