from aiohttp import web
from loguru import logger
from pydantic import BaseModel
from datetime import date
import uuid

from common import connect_db
from dog_repository import DogsCRUD
from model import *

app_state: dict[str, any] = dict()


"""
AI:

Create a aiohttp application with paths corresponding to all CRUD operations from the class DogsCRUD:



class DogsCRUD:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def create_dog(self, dog: Dog) -> Dog:
        async with self.pool.acquire() as connection:
            query = "INSERT INTO dogs (id, breed_id, lineage, birthdate, name) VALUES ($1, $2, $3, $4, $5) RETURNING *"
            record = await connection.fetchrow(query, dog.id, dog.breed_id, dog.lineage, dog.birthdate, dog.name)
            return Dog(**record)

    async def read_dog(self, dog_id: uuid.UUID) -> Dog | None:
        async with self.pool.acquire() as connection:
            query = "SELECT * FROM dogs WHERE id = $1"
            record = await connection.fetchrow(query, dog_id)
            return Dog(**record) if record else None

    async def update_dog(self, dog_id: uuid.UUID, dog: Dog) -> None:
        async with self.pool.acquire() as connection:
            query = "UPDATE dogs SET breed_id = $1, lineage = $2, birthdate = $3, name = $4 WHERE id = $5"
            await connection.execute(query, dog.breed_id, dog.lineage, dog.birthdate, dog.name, dog_id)

    async def delete_dog(self, dog_id: uuid.UUID) -> None:
        async with self.pool.acquire() as connection:
            query = "DELETE FROM dogs WHERE id = $1"
            await connection.execute(query, dog_id)

where


from pydantic import BaseModel


class Dog(BaseModel):
    id: UUID | None
    breed_id: UUID
    lineage: str
    birthdate: date
    name: str

"""


# ------------------------------- GENERATED CODE


# Create a new dog
async def create_dog(request):
    data = await request.json()
    new_dog = Dog(**data)
    created_dog = await dogs_crud().create_dog(new_dog)
    return web.json_response(created_dog.dict())


# Get a dog by ID
async def get_dog(request):
    dog_id = request.match_info['dog_id']
    dog = await dogs_crud().read_dog(uuid.UUID(dog_id))
    if dog:
        return web.json_response(dog.dict())
    else:
        return web.Response(status=404)


# Update a dog by ID
async def update_dog(request):
    dog_id = request.match_info['dog_id']
    data = await request.json()
    updated_dog = Dog(**data)
    await dogs_crud().update_dog(uuid.UUID(dog_id), updated_dog)
    return web.Response(status=204)


# Delete a dog by ID
async def delete_dog(request):
    dog_id = request.match_info['dog_id']
    await dogs_crud().delete_dog(uuid.UUID(dog_id))
    return web.Response(status=204)


# --------------------- END OF GENERATED CODE ------------------------
# todo: above -- must replace "dogs_crud" with function call "dogs_crud()"

# ------------------ code written per hand:

def dogs_crud() -> DogsCRUD:
    return app_state["dogs_crud"]


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()

    # Add routes to the application
    app.router.add_post('/dogs', create_dog)
    app.router.add_get('/dogs/{dog_id}', get_dog)
    app.router.add_put('/dogs/{dog_id}', update_dog)
    app.router.add_delete('/dogs/{dog_id}', delete_dog)

    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    app_state["dogs_crud"] = DogsCRUD(pool)

    print('db connected')
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
