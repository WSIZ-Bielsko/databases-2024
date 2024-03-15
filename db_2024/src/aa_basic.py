import aiohttp
from aiohttp import web


async def hello(request):
    return web.json_response({'message': 'Hello, welcome to the aiohttp app!'})


async def add(request):
    data = await request.json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    print(f'request to add two numbers: {a=}, {b=}')
    result = a + b
    return web.json_response({'result': result})


app = web.Application()
app.router.add_get('/hello', hello)
app.router.add_post('/add', add)

if __name__ == '__main__':
    web.run_app(app, port=8087)
