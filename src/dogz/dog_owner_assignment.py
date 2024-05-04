from asyncio import run
from random import choice
from uuid import uuid4

from faker import Faker
from loguru import logger

from common import connect_db
from model import Person, Dog
from dog_repository import DogsCRUD
from person_repository import PersonCRUD


async def assign_owners_randomly(
    dogs_repo: DogsCRUD, persons_repo: PersonCRUD, n_assignments: int
):
    logger.info(f"assigning {n_assignments} owners randomly: start")
    dog_ids = [d.id for d in await dogs_repo.read_all()]
    person_ids = [p.id for p in await persons_repo.read_all()]

    for _ in range(n_assignments):
        did = choice(dog_ids)
        pid = choice(person_ids)
        await dogs_repo.assign_person_to_dog(person_id=pid, dog_id=did)
        logger.debug(f"assigned {pid} as owner of {did}")

    logger.info(f"assigning {n_assignments} owners randomly: complete")


async def generate_random_dogs(dogs_repo: DogsCRUD, n_dogs: int):
    fake = Faker()
    for _ in range(n_dogs):
        d = Dog(
            id=uuid4(),
            breed_id=uuid4(),
            lineage=fake.name(),
            birthdate=fake.date_time_between(start_date="-4d", end_date="now").date(),
            name=fake.name(),
        )
        await dogs_repo.create_dog(d)
        logger.debug(f"dog {d} saved")


async def generate_random_persons(person_repo: PersonCRUD, n_persons: int):
    fake = Faker()
    for _ in range(n_persons):
        p = Person(
            id=uuid4(), pesel=fake.ssn(), name=fake.name(), phone=fake.phone_number()
        )
        await person_repo.create(p)
        logger.debug(f"person {p} saved")


async def main():
    DATABASE_URL = "postgres://postgres:postgres@10.10.1.200:5432/postgres"
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print("db connected")
    repoDogs = DogsCRUD(pool=pool)
    repoPers = PersonCRUD(pool=pool)
    # await generate_random_dogs(repoDogs, n_dogs=1000)
    # await generate_random_persons(repoPers, n_persons=300)
    await assign_owners_randomly(repoDogs, repoPers, n_assignments=300)


if __name__ == "__main__":
    run(main())
