from loguru import logger

from src.remote_tasks.model import JobRequest, User, Volume, VolumeClaim, Node, NodeState, Job, Log

"""
preplexity.ai prompt

Write a class EntityRepository with methods for CRUD operations using asyncpg
for the following pydantic data class:


class Log(BaseModel):
    id: UUID
    job_id: UUID
    timestamp: datetime
    stream: str  # stdout or stderr
    level: str
    message: str

Apart from the method corresponding to delete operation, all other ms should return 
instance or instances of the dataclass or None.

Assume connection pool is assigned in constructor of EntityRepository.

In the result, replace "Optional" by " | None" python construct.  

Create instances of the dataclass by (**result) code. 

Use `select *` in list and get methods. 

Use modern python syntax (python >= 3.11), don't use the typing package. 

In update method use "returning *" in sql. 

Use singular for table name in sql. 

The methods should have a suffix equal to the dataclass name. 
"""
import asyncpg
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
                    INSERT INTO JobRequest (
                        id, repo_url, commit, image_tag, entry_point_file,
                        env_file_content, cpu, ram_mb, priority, user_id, submitted_at, started_at, cancelled_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                    RETURNING *
                    """,
                    job_request.id, job_request.repo_url, job_request.commit, job_request.image_tag,
                    job_request.entry_point_file, job_request.env_file_content, job_request.cpu,
                    job_request.ram_mb, job_request.priority, job_request.user_id,
                    job_request.submitted_at,
                    job_request.started_at,
                    job_request.cancelled_at
                )
                return JobRequest(**row)

    async def create_multiple_task(self, job_reqs: list[JobRequest]):
        async with self.pool.acquire() as conn:
            logger.info(f'Creating {len(job_reqs)}')
            query = """
                INSERT INTO JobRequest (
                    id, repo_url, commit, image_tag, entry_point_file,
                    env_file_content, cpu, ram_mb, priority, user_id, submitted_at, started_at, cancelled_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """
            data = [(
                r.id, r.repo_url, r.commit, r.image_tag, r.entry_point_file,
                r.env_file_content, r.cpu, r.ram_mb, r.priority, r.user_id,
                r.submitted_at, r.started_at, r.cancelled_at
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
            return [JobRequest(**row) for row in rows]

    async def update_task(self, job_request: JobRequest) -> JobRequest | None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    """
                    UPDATE JobRequest
                    SET repo_url = $2, commit = $3, image_tag = $4, entry_point_file = $5,
                        env_file_content = $6, cpu = $7, ram_mb = $8, priority = $9,
                        user_id = $10, submitted_at = $11, started_at=$12, cancelled_at = $13
                    WHERE id = $1
                    RETURNING *
                    """,
                    job_request.id, job_request.repo_url, job_request.commit, job_request.image_tag,
                    job_request.entry_point_file, job_request.env_file_content, job_request.cpu,
                    job_request.ram_mb, job_request.priority, job_request.user_id,
                    job_request.submitted_at,
                    job_request.started_at,
                    job_request.cancelled_at
                )
                if row:
                    return JobRequest(**row)
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

    async def create_multiple_users(self, users: list[User]):
        async with self.pool.acquire() as conn:
            logger.info(f'Creating {len(users)} users')
            query = """
                    INSERT INTO users (
                        id, name
                    )
                    VALUES ($1, $2)
                    """
            data = [(user.id, user.name) for user in users]
            await conn.executemany(query, data)
            logger.info(f'Creating {len(users)} users complete')

    async def read_user(self, user_id: UUID) -> User | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM "users" WHERE id = $1
                """,
                user_id
            )
            if row:
                return User(**row)
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

    # volumes

    async def create_volume(self, volume: Volume) -> Volume | None:
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO volume (id, name) 
            VALUES ($1, $2) 
            RETURNING id, name
            """
            result = await connection.fetchrow(query, volume.id, volume.name)
            if result:
                return Volume(**result)
            return None

    async def get_volume(self, volume_id: UUID) -> Volume | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM volume WHERE id = $1"
            result = await connection.fetchrow(query, volume_id)
            if result:
                return Volume(**result)
            return None

    async def update_volume(self, volume: Volume) -> Volume | None:
        async with self.pool.acquire() as connection:
            query = """
            UPDATE volume
            SET name = $2 
            WHERE id = $1 
            RETURNING *
            """
            result = await connection.fetchrow(query, volume.id, volume.name)
            if result:
                return Volume(**result)
            return None

    async def delete_volume(self, volume_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM volume WHERE id = $1"
            result = await connection.execute(query, volume_id)
            return result == "DELETE 1"

    async def list_volumes(self) -> list[Volume]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM volume"
            results = await connection.fetch(query)
            return [Volume(**result) for result in results]

    # volume claims

    async def create_volume_claim(self, volume_claim: VolumeClaim) -> VolumeClaim | None:
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO volumeclaim (id, volume_id, job_request_id, mount_type)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """
            result = await connection.fetchrow(query, volume_claim.id, volume_claim.volume_id,
                                               volume_claim.job_request_id, volume_claim.mount_type)
            if result:
                return VolumeClaim(**result)
            return None

    async def get_volume_claim(self, volume_claim_id: UUID) -> VolumeClaim | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM volumeclaim WHERE id = $1"
            result = await connection.fetchrow(query, volume_claim_id)
            if result:
                return VolumeClaim(**result)
            return None

    async def update_volume_claim(self, volume_claim: VolumeClaim) -> VolumeClaim | None:
        async with self.pool.acquire() as connection:
            query = """
            UPDATE volumeclaim
            SET volume_id = $2, job_request_id = $3, mount_type = $4
            WHERE id = $1
            RETURNING *
            """
            result = await connection.fetchrow(query, volume_claim.id, volume_claim.volume_id,
                                               volume_claim.job_request_id, volume_claim.mount_type)
            if result:
                return VolumeClaim(**result)
            return None

    async def delete_volume_claim(self, volume_claim_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM volumeclaim WHERE id = $1"
            result = await connection.execute(query, volume_claim_id)
            return result == "DELETE 1"

    async def list_volume_claims(self) -> list[VolumeClaim]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM volumeclaim"
            results = await connection.fetch(query)
            return [VolumeClaim(**result) for result in results]

    # node

    async def create_node(self, node: Node) -> Node | None:
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO node (id, name, max_cpu, max_ram)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """
            result = await connection.fetchrow(query, node.id, node.name, node.max_cpu, node.max_ram)
            if result:
                logger.info(f'node {node.name} created')
                return Node(**result)
            return None

    async def get_node(self, node_id: UUID) -> Node | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM node WHERE id = $1"
            result = await connection.fetchrow(query, node_id)
            if result:
                return Node(**result)
            return None

    async def update_node(self, node: Node) -> Node | None:
        async with self.pool.acquire() as connection:
            query = """
            UPDATE node
            SET name = $2, max_cpu = $3, max_ram = $4
            WHERE id = $1
            RETURNING *
            """
            result = await connection.fetchrow(query, node.id, node.name, node.max_cpu, node.max_ram)
            if result:
                return Node(**result)
            return None

    async def delete_node(self, node_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM node WHERE id = $1"
            result = await connection.execute(query, node_id)
            return result == "DELETE 1"

    async def list_nodes(self) -> list[Node]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM node"
            results = await connection.fetch(query)
            return [Node(**result) for result in results]

    # node state

    async def create_node_state(self, node_state: NodeState) -> NodeState | None:
        async with self.pool.acquire() as connection:
            query = """
            INSERT INTO node_state (id, node_id, reported_at, used_cpu, used_ram)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """
            result = await connection.fetchrow(query, node_state.id, node_state.node_id, node_state.reported_at,
                                               node_state.used_cpu, node_state.used_ram)
            if result:
                return NodeState(**result)
            return None

    async def get_node_state(self, node_state_id: UUID) -> NodeState | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM node_state WHERE id = $1"
            result = await connection.fetchrow(query, node_state_id)
            if result:
                return NodeState(**result)
            return None

    async def update_node_state(self, node_state: NodeState) -> NodeState | None:
        async with self.pool.acquire() as connection:
            query = """
            UPDATE node_state
            SET node_id = $2, reported_at = $3, used_cpu = $4, used_ram = $5
            WHERE id = $1
            RETURNING *
            """
            result = await connection.fetchrow(query, node_state.id, node_state.node_id, node_state.reported_at,
                                               node_state.used_cpu, node_state.used_ram)
            if result:
                return NodeState(**result)
            return None

    async def delete_node_state(self, node_state_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM node_state WHERE id = $1"
            result = await connection.execute(query, node_state_id)
            return result == "DELETE 1"

    async def list_node_states(self) -> list[NodeState]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM node_state"
            results = await connection.fetch(query)
            return [NodeState(**result) for result in results]

    # job

    async def create_job(self, job: Job) -> Job | None:
        async with self.pool.acquire() as connection:
            query = """
               INSERT INTO job (id, request_id, node_id, started_at, canceled_at, finished_at)
               VALUES ($1, $2, $3, $4, $5, $6)
               RETURNING *
               """
            result = await connection.fetchrow(query, job.id, job.request_id, job.node_id, job.started_at,
                                               job.canceled_at, job.finished_at)
            if result:
                logger.info(f'job {job.id} created')
                return Job(**result)
            return None

    async def create_multiple_jobs(self, jobs: list[Job]):
        async with self.pool.acquire() as conn:
            logger.info(f'Creating {len(jobs)} jobs')
            query = """
                INSERT INTO job (
                    id, request_id, node_id, started_at, canceled_at, finished_at
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                """
            data = [(
                job.id, job.request_id, job.node_id, job.started_at,
                job.canceled_at, job.finished_at
            ) for job in jobs]

            await conn.executemany(query, data)
            logger.info(f'Creating {len(jobs)} jobs complete')

    async def get_job(self, job_id: UUID) -> Job | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM job WHERE id = $1"
            result = await connection.fetchrow(query, job_id)
            if result:
                return Job(**result)
            return None

    async def update_job(self, job: Job) -> Job | None:
        async with self.pool.acquire() as connection:
            query = """
               UPDATE job
               SET request_id = $2, node_id = $3, started_at = $4, canceled_at = $5, finished_at = $6
               WHERE id = $1
               RETURNING *
               """
            result = await connection.fetchrow(query, job.id, job.request_id, job.node_id, job.started_at,
                                               job.canceled_at, job.finished_at)
            if result:
                return Job(**result)
            return None

    async def delete_job(self, job_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM job WHERE id = $1"
            result = await connection.execute(query, job_id)
            return result == "DELETE 1"

    async def list_jobs(self) -> list[Job]:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM job"
            results = await connection.fetch(query)
            return [Job(**result) for result in results]

    # log

    async def create_log(self, log: Log) -> Log | None:
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(
                """
                INSERT INTO log (id, job_id, logged_at, stream, level, message)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
                """,
                log.id, log.job_id, log.logged_at, log.stream, log.level, log.message
            )
            return Log(**result) if result else None

    async def get_log(self, log_id: UUID) -> Log | None:
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(
                "SELECT * FROM Log WHERE id = $1", log_id
            )
            return Log(**result) if result else None

    async def list_log(self) -> list[Log]:
        # todo: deprecated; create more specific listing method
        async with self.pool.acquire() as connection:
            results = await connection.fetch("SELECT * FROM Log")
            return [Log(**result) for result in results]

    async def update_log(self, log: Log) -> Log | None:
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(
                """
                UPDATE Log
                SET job_id = $2, logged_at = $3, stream = $4, level = $5, message = $6
                WHERE id = $1
                RETURNING *
                """,
                log.id, log.job_id, log.logged_at, log.stream, log.level, log.message
            )
            return Log(**result) if result else None

    async def delete_log(self, log_id: UUID) -> None:
        async with self.pool.acquire() as connection:
            await connection.execute("DELETE FROM Log WHERE id = $1", log_id)

    # misc

    async def get_recent_requests_of_users(self, user_ids: list[UUID], days: int) -> list[JobRequest]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                select * from jobrequest 
                where submitted_at > now() - ($2 || ' days')::INTERVAL AND
                user_id = ANY ($1::uuid[]) 
                """, user_ids, str(days))
            return [JobRequest(**row) for row in rows]

    async def list_unscheduled_job_requests(self, limit: int) -> list[JobRequest]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                select  *
                from jobrequest 
                where started_at is null
                order by priority desc, submitted_at
                limit $1;
                """, limit)
            return [JobRequest(**row) for row in rows]

    async def list_running_jobs(self, limit) -> list[Job]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                    select *
                    from job
                    where finished_at is NULL
                      and canceled_at is NULL
                    order by started_at
                    limit $1;
                """, limit)
            return [Job(**row) for row in rows]
