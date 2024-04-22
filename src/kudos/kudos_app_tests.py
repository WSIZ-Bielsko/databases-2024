from uuid import UUID, uuid4

import requests
from loguru import logger

from model import *

URL = 'http://localhost:5000'


def create_dog(dog: Dog):
    url = f'{URL}/dogs'
    res = requests.post(url, json=dog.dict())
    logger.debug(f'create -> {res.status_code}')


def get_dog(id: UUID) -> Dog | None:
    logger.info(f'getting dog with {id=}')
    url = f'{URL}/dogs/{id}'
    res = requests.get(url)
    logger.debug(f'get -> {res.status_code}')
    z = res.json()
    return Dog(**z)


def update_dog(dog: Dog):
    url = f'{URL}/dogs/{dog.id}'
    res = requests.put(url, json=dog.dict())  # no data in response
    logger.debug(f'update -> {res.status_code}')


def delete_dog(dog_id: UUID):
    url = f'{URL}/dogs/{dog_id}'
    res = requests.delete(url)  # no data in response
    logger.debug(f'delete -> {res.status_code}')


if __name__ == '__main__':
    dog = get_dog(id=UUID('b7a1b679-9bff-4eb1-9cca-b7eb5e78eb8f'))
    logger.info(dog)
    dog.name = 'Luna'
    update_dog(dog)
    dog.name = 'Szarik'
    update_dog(dog)

    new_dog = Dog(id=uuid4(), breed_id=uuid4(), lineage='N/A', birthdate=date(1969, 1, 24), name='Scooby Doo')
    create_dog(new_dog)
    new_dog.lineage = 'Extinct'
    update_dog(new_dog)
    delete_dog(new_dog.id)
