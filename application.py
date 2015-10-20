from os import environ
from asyncio import get_event_loop

from aiohttp import web

async def handle(request):
    return web.Response(body='hello'.encode())

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', environ['PORT'])
    return srv


loop = get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
