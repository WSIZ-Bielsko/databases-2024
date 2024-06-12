import datetime
from asyncio import run
from random import randint, choice
from uuid import uuid4, UUID

from loguru import logger

from src.remote_tasks.common import connect_db
from src.remote_tasks.model import User, JobRequest, Volume, VolumeClaim, Node, NodeState
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
                               submitted_at=None, cancelled_at=None)
                    for i in range(BATCH_SIZE)]
        await repo.create_multiple_task(job_reqs)


async def main():
    pool = await connect_db()
    repo = TaskCrudRepository(pool)
    # await create_users(n_users=30, repo=repo)
    users = await repo.read_all_users()
    await create_job_requests(users=users, n_requests=1 * 10 ** 5, repo=repo)

    # for i in range(100):
    #     vol = Volume(id=uuid4(), name=f'volume{i}')
    #     v = await repo.create_volume(vol)

    # job_request b03f5933-77f8-485e-9244-90640a284618
    # vol_claim = VolumeClaim(id=uuid4(),
    #                         volume_id=UUID('037b6813-efb6-4b92-8aaa-c13719e2ce29'),
    #                         job_request_id=UUID('b03f5933-77f8-485e-9244-90640a284618'),
    #                         mount_type='RW')
    # created = await repo.create_volume_claim(vol_claim)
    #
    # saved = await repo.get_volume_claim(created.id)
    # assert created == saved
    # claims = await repo.list_volume_claims()
    # print(claims)

    # node = Node(id=uuid4(), name='nodeX', max_cpu=32, max_ram=1024)
    # n = await repo.create_node(node)
    # print(n)  # UUID('31148731-814f-4e34-98c7-07139f8238c2')

    # nstate = NodeState(id=uuid4(), node_id=UUID('31148731-814f-4e34-98c7-07139f8238c2'),
    #                    reported_at=datetime.datetime.now(), used_cpu=3.5, used_ram=512)
    # saved = await repo.create_node_state(nstate)
    # print(saved)

    # reqs = await repo.get_recent_requests_of_users(
    #     user_ids=[UUID('947b3582-1147-4347-8038-8f0f86f4fb89'),
    #               UUID('695c4a66-23b4-414c-a95c-ca9348f7068b')], days=120)
    # print(reqs)


if __name__ == '__main__':
    run(main())
