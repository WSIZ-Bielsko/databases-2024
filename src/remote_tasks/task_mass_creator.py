from asyncio import run
from random import randint, choice
from uuid import uuid4

from loguru import logger

from src.remote_tasks.common import connect_db
from src.remote_tasks.model import User, JobRequest
from src.remote_tasks.task_crud_repositories import TaskCrudRepository


async def create_users(n_users: int, repo: TaskCrudRepository):
    for _ in range(n_users):
        u = User(id=uuid4(), name=f'user{randint(1, 10 ** 6)}')
        await repo.create_user(u)


async def create_job_requests(users: list[User], n_requests: int, repo: TaskCrudRepository):
    user_ids = [u.id for u in users]
    BATCH_SIZE = 10 ** 4
    n_batches = (n_requests + BATCH_SIZE - 1) // BATCH_SIZE

    for b in range(n_batches):
        logger.info(f'Starting job requests creation batch number {b}/{n_batches}')
        job_reqs = [JobRequest(id=uuid4(),
                               repo_url='https://example.com',
                               commit=f'abc{randint(1, 10 ** 6)}',
                               image_tag='',
                               entry_point_file='a.py',
                               env_file_content='',
                               cpu=0.5 * randint(1, 4),
                               ram_mb=randint(1, 16),
                               priority=randint(1, 5),
                               user_id=choice(user_ids),
                               submitted_at=None)
                    for i in range(BATCH_SIZE)]
        await repo.create_multiple_task(job_reqs)


async def main():
    pool = await connect_db()
    repo = TaskCrudRepository(pool)
    # await create_users(n_users=30, repo=repo)
    users = await repo.read_all_users()
    await create_job_requests(users=users, n_requests=3 * 10 ** 5, repo=repo)


if __name__ == '__main__':
    run(main())
