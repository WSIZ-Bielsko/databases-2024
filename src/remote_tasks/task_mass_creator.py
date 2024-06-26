from datetime import datetime
from asyncio import run, gather
from random import randint, choice, sample
from uuid import uuid4, UUID

from loguru import logger

from src.remote_tasks.common import connect_db
from src.remote_tasks.model import User, JobRequest, Volume, VolumeClaim, Node, NodeState, Job
from src.remote_tasks.task_crud_repositories import TaskCrudRepository


async def create_users(n_users: int, repo: TaskCrudRepository):
    for _ in range(n_users):
        u = User(id=uuid4(), name=f'user{randint(1, 10 ** 6)}')
        await repo.create_user(u)


async def create_nodes(n_nodes: int, repo: TaskCrudRepository):
    for _ in range(n_nodes):
        n = Node(id=uuid4(), name=f'node{randint(1, 10 ** 6)}',
                 max_cpu=4 * randint(1, 16), max_ram=16 * randint(1, 16))
        await repo.create_node(n)


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
                               submitted_at=None, started_at=None, cancelled_at=None)
                    for i in range(BATCH_SIZE)]
        await repo.create_multiple_task(job_reqs)


async def schedule_job(n_jobs: int, repo: TaskCrudRepository):
    async with repo.pool.acquire() as conn:
        async with conn.transaction():
            logger.debug('transaction begin')
            nodes = await repo.list_nodes()

            jrs = await repo.list_unscheduled_job_requests(limit=1)
            # ↑↑ should take "connection" as parameter -- preserve transaction

            for jr in jrs:
                node = choice(nodes)
                # todo: can only be placed on node with enough resources
                # plan this as a series of SQL's
                job = Job(id=uuid4(), request_id=jr.id,
                          node_id=node.id,
                          started_at=datetime.now(),
                          canceled_at=None,
                          finished_at=None)
                logger.info(f'job request {jr.id} to be scheduled for node {node.id}')
                jr.started_at = datetime.now()
                await repo.create_job(job, conn)  #fixme: 1) save to job table

                # what if node is now fully occupied?
                await repo.update_task(jr, conn)  #fixme: 2) save to jobrequest table
                # what if sb. cancelled it befeore it was scheduled

                # fixme add: 3) update node table
                node.used_cpu -= jr.cpu
                node.used_ram -= jr.ram_mb
                await repo.update_node(node, conn)



            logger.debug('transaction closed')
        logger.info(f'job scheduling for {n_jobs} complete')


async def complete_random_jobs(n_jobs: int, repo: TaskCrudRepository):
    running_jobs = await repo.list_running_jobs(n_jobs)
    for j in sample(running_jobs, k=n_jobs):
        j.finished_at = datetime.now()
        await repo.update_job(j)
        logger.info(f'job {j.id} finished successfully')


async def main():
    pool = await connect_db()
    repo = TaskCrudRepository(pool)
    # await create_users(n_users=30, repo=repo)
    # users = await repo.read_all_users()
    # await create_job_requests(users=users, n_requests=1 * 10 ** 5, repo=repo)

    # await schedule_job(n_jobs=1000, repo=repo)
    # await complete_random_jobs(n_jobs=20, repo=repo)

    ids = await repo.retrieve_venerated_job_ids_by_volume_id(UUID('efd2f5e7-5ad8-485c-9180-1a57266ea974'))
    for i in ids:
        print(i)
    # await create_nodes(n_nodes=8, repo=repo)

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


if __name__ == '__main__':
    run(main())
