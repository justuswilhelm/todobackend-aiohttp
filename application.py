from asyncio import get_event_loop
from logging import getLogger, basicConfig, INFO
from os import environ

from aiohttp import web

basicConfig(level=INFO)
logger = getLogger(__name__)

async def handle(request):
    return web.Response(body='hello'.encode())

async def init(loop):
    app = web.Application(
        loop=loop,
        middlewares=[
        cors_middleware_factory
    ])

    # Routes
    app.router.add_route('GET', '/', handle)
    app.router.add_route('OPTIONS', '/', handle)

    handler = app.make_handler()

    # Config
    ip = '0.0.0.0'
    port = environ['PORT']

    logger.info("Starting server at %s:%s", ip, port)
    srv = await loop.create_server(
        handler, ip, port)
    return srv


async def cors_middleware_factory(app, handler):
    async def middleware(request):
        resp = await handler(request)
        resp.headers.update({
            'Access-Control-Allow-Origin': '*',
        })
        return resp
    return middleware


loop = get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
