import random

from aiohttp import web
from loguru import logger

from src.corporate_vote.db_repository import DbRepository, connect_db

tokens_2_shares = dict()
voted = set()
result = {'total_yes': 0, 'total_no': 0, 'total_abst': 0}
state = {}


def db() -> DbRepository:
    return state['db']


async def handle_create(request):
    logger.info('Vote reset')
    new_vote = await db().create_new_vote()
    return web.json_response(data={
        "status": "success",
        "message": "Vote created",
        "vote_id": new_vote.vote_id
    })


async def handle_result(request):
    vote_id = int(request.query.get('vote_id'))

    logger.info(f'Vote results for {vote_id}:')
    results = await db().get_results(vote_id)

    return web.json_response(data={
        "status": "success",
        "message": f"Vote results fetched",
        "results": results.json()
    })


async def handle_vote(request):
    token = request.query.get('token')
    vote = request.query.get('vote')
    vote_id = int(request.query.get('vote_id'))

    user = await db().get_user_by_token(token)
    if user is None:
        logger.warning(f'Invalid token {token} voting')
        return web.json_response(data={
            "status": "error",
            "message": "Invalid token",
        })
    participated = await db().has_participated(user.email, vote_id)
    if participated:
        logger.warning(f'Token {token} already voted')
        return web.json_response(data={
            "status": "error",
            "message": "Token already used",
        })

    await db().vote(token, vote, vote_id)

    return web.json_response(data={
        "status": "success",
        "message": "Vote recorded",
    })


async def handle_login(request):
    email = request.query.get('email')
    password = request.query.get('password')

    try:
        token = await db().login(email, password)
    except Exception as e:
        logger.warning(e)
        return web.json_response(data={
            "status": "error",
            "message": "Invalid login credentials",
        })

    return web.json_response(data={
        "status": "success",
        "message": "Login successful",
        "token": token
    })


async def main():
    state['db'] = DbRepository(await connect_db())
    app = web.Application()
    app.router.add_get('/create', handle_create)
    app.router.add_get('/result', handle_result)
    app.router.add_get('/vote', handle_vote)
    app.router.add_get('/login', handle_login)
    return app


if __name__ == '__main__':
    web.run_app(main(), port=9090)
