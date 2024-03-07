import os
from platform import node
from uuid import UUID

from aiohttp import web
from loguru import logger

from model import User, PlanItem
from db_service import DbService, DEFAULT_DATABASE_URL

routes = web.RouteTableDef()

app_state: dict[str, any] = dict()
app_state['users'] = dict()  # userid -> user


def db() -> DbService:
    """
    Alias -- helps with syntax completion
    :return: DbService used by the application
    """
    return app_state['db']


@routes.get('/')
async def hello(request):
    logger.info(f'/ hit on host {node()}')
    return web.json_response({'comment': f'hello from {node()}; nice to answer your call!'})


# add /greet?name=... ; default: user; greet him


@routes.post('/plan-item')
async def create_plan_item(request):
    logger.info(f'PI /create hit')
    item = await request.json()
    item = PlanItem(**item)
    logger.debug('PI properly parsed')
    created = await db().create_plan(item)
    return web.json_response(created.dict(), status=200)


@routes.put('/plan-item')
async def create_plan_item(request):
    logger.info(f'PI /update hit')
    item = await request.json()
    item = PlanItem(**item)
    logger.debug('PI properly parsed')
    updated = await db().update_plan(item)
    return web.json_response(updated.dict(), status=200)


@routes.get('/users/{uid}')
async def get_user_with_id(request):
    logger.info('GET /users/{uid} hit')
    try:
        user_id = UUID(request.match_info['uid'])
    except RuntimeError:
        return web.json_response({'result': f'No user id provided', 'host': node()}, status=400)

    logger.info(f'Getting user with id={user_id}')

    user = await db().get_user_by_uid(user_id)

    if not user:
        return web.json_response({'result': f'No user id={user_id} exists', 'host': node()}, status=400)
    return web.json_response(user.serialized(), status=200)


async def app_factory():
    """
    Function run at the startup of the application. If some async initialization is needed - put it in here.
    i.e. we can initialize database connection here...
    """
    app = web.Application()
    app.add_routes(routes)
    DATABASE_URL = os.getenv('DB_URL', DEFAULT_DATABASE_URL)
    app_state['db'] = DbService(DATABASE_URL)
    await db().initialize()
    return app


if __name__ == '__main__':
    web.run_app(app_factory(), port=5000)
