import asyncpg
from aiohttp import web

from dog_repository import DogsCRUD, Dog


async def create_dog(request):
    data = await request.json()
    new_dog = Dog(**data)
    dog_id = await request.app['crud'].create_dog(new_dog)
    return web.json_response({'id': dog_id})


async def read_dog(request):
    dog_id = int(request.match_info['dog_id'])
    dog = await request.app['crud'].get_dog(dog_id)
    return web.json_response(dog.dict())


async def update_dog(request):
    dog_id = int(request.match_info['dog_id'])
    data = await request.json()
    updated_dog = Dog(**data)
    await request.app['crud'].update_dog(dog_id, updated_dog)
    return web.Response(status=200)


async def delete_dog(request):
    dog_id = int(request.match_info['dog_id'])
    await request.app['crud'].delete_dog(dog_id)
    return web.Response(status=200)


async def init_app():
    app = web.Application()

    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'

    pool = await asyncpg.create_pool(dsn=DATABASE_URL)
    print('pool created')
    app['db_pool'] = pool
    app['crud'] = DogsCRUD(pool)
    print('DogsCRUD created')

    app.router.add_post('/dogs', create_dog)
    app.router.add_get('/dogs/{dog_id}', read_dog)
    app.router.add_put('/dogs/{dog_id}', update_dog)
    app.router.add_delete('/dogs/{dog_id}', delete_dog)

    return app

if __name__ == '__main__':
    web.run_app(init_app(), port=8081)