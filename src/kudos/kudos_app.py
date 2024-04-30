import os
from uuid import UUID
from aiohttp import web
from asyncpg import Pool
from loguru import logger

from src.kudos.common import connect_db
from src.kudos.kudo_repository import KudoRepository
from src.kudos.model import Kudo

app_state: dict[str, any] = dict()


# ------------------------------- STANDARD CRUD via HTTP


# Create a new dog
async def create_kudo(request):
    data = await request.json()
    kudo = Kudo(**data)
    created = await kudo_repo().create(kudo)
    return web.json_response(created.dict())


# Get a dog by ID
async def get_kudo(request):
    dog_id = request.match_info['id']
    dog = await kudo_repo().read(UUID(dog_id))
    if dog:
        return web.json_response(dog.dict())
    else:
        return web.Response(status=404)


# Update a dog by ID
async def update_kudo(request):
    data = await request.json()
    kudo = Kudo(**data)
    await kudo_repo().update(kudo)
    return web.Response(status=204)


# Delete a dog by ID
async def delete_kudo(request):
    dog_id = request.match_info['id']
    await kudo_repo().delete(UUID(dog_id))
    return web.Response(status=204)


# --------------------- END OF STANDARD CRUD via HTTP ------------------------

async def status(request):
    return web.json_response({'status': 'ok'})


def kudo_repo() -> KudoRepository:
    return app_state["kudo_repo"]


async def app_factory(pool: Pool = None):
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()

    # Add routes to the application
    app.router.add_get('/status', status)
    app.router.add_post('/dogs', create_kudo)
    app.router.add_get('/dogs/{dog_id}', get_kudo)
    app.router.add_put('/dogs/{dog_id}', update_kudo)
    app.router.add_delete('/dogs/{dog_id}', delete_kudo)

    if pool is None:
        pool = await connect_db()
    app_state["kudo_repo"] = KudoRepository(pool)

    print('db connected')
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
