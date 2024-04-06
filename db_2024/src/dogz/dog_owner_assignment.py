from asyncio import run
from random import choice

from loguru import logger

from common import connect_db
from dog_repository import DogsCRUD
from person_repository import PersonCRUD


async def assign_owners_randomly(dogs_repo: DogsCRUD, persons_repo: PersonCRUD, n_assignments: int):
    logger.info(f'assigning {n_assignments} owners randomly: start')
    dog_ids = [d.id for d in await dogs_repo.read_all()]
    person_ids = [p.id for p in await persons_repo.read_all()]

    for _ in range(n_assignments):
        did = choice(dog_ids)
        pid = choice(person_ids)
        await dogs_repo.assign_person_to_dog(person_id=pid, dog_id=did)
        logger.debug(f'assigned {pid} as owner of {did}')

    logger.info(f'assigning {n_assignments} owners randomly: complete')


async def main():
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repoDogs = DogsCRUD(pool=pool)
    repoPers = PersonCRUD(pool=pool)
    await assign_owners_randomly(repoDogs, repoPers, n_assignments=100)


if __name__ == '__main__':
    run(main())
