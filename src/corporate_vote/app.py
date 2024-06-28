import random

from aiohttp import web
from loguru import logger

tokens_2_shares = dict()
voted = set()
result = {'total_yes': 0, 'total_no': 0, 'total_abst': 0}


def assign_tokens():
    random_keys = random.sample(range(1000, 10000), 6)

    # Create the dictionary
    random_dict = {
        random_keys[0]: 30,
        random_keys[1]: 30,
        random_keys[2]: 25,
        random_keys[3]: 15
    }
    for (k, v) in random_dict.items():
        print(k, v)
        tokens_2_shares[str(k)] = v


async def handle_reset(request):
    logger.info('Vote reset')
    voted.clear()
    for k in result.keys():
        result[k] = 0
    return web.json_response(data={
        "status": "success",
        "message": "Vote reset",
    })


async def handle_result(request):
    logger.info('Vote results:')
    logger.info(f'Tokens voted: {len(voted)}')
    logger.info(f'Results: {result}')

    return web.json_response(data={
        "status": "success",
        "message": f"Vote result: {result}",
    })


async def handle_vote(request):
    token = request.query.get('token')
    vote = request.query.get('vote')

    if token not in tokens_2_shares:
        logger.warning(f'Invalid token {token} voting')
        return web.json_response(data={
            "status": "error",
            "message": "Invalid token",
        })
    elif token in voted:
        logger.warning(f'Token {token} already voted')
        return web.json_response(data={
            "status": "error",
            "message": "Token already used",
        })
    else:
        voted.add(token)
        if vote == 'yes':
            result['total_yes'] += tokens_2_shares[token]
        elif vote == 'no':
            result['total_no'] += tokens_2_shares[token]
        elif vote == 'pass':
            result['total_abst'] += tokens_2_shares[token]
        else:
            logger.warning(f'Invalid vote {vote} from token {token}')
            voted.remove(token)
            return web.json_response(data={
                "status": "error",
                "message": "Wrong vote parameter",
            })

    return web.json_response(data={
        "status": "success",
        "message": "Vote recorded",
    })


async def main():
    app = web.Application()
    app.router.add_get('/vote', handle_vote)
    app.router.add_get('/reset', handle_reset)
    app.router.add_get('/result', handle_result)
    return app


if __name__ == '__main__':
    assign_tokens()
    web.run_app(main(), port=9090)
