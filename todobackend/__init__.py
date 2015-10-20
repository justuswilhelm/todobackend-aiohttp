from logging import getLogger, basicConfig, INFO
from os import environ
from aiohttp import web

from .views import (
    IndexView,
    TodoView,
)

IP = '0.0.0.0'
PORT = environ['PORT']

basicConfig(level=INFO)
logger = getLogger(__name__)


async def init(loop):
    app = web.Application(loop=loop, middlewares=[cors_middleware_factory])

    # Routes
    app.router.add_route('*', '/', IndexView.dispatch)

    app.router.add_route('*', '/{uuid}', TodoView.dispatch)

    # Config
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv


async def cors_middleware_factory(app, handler):
    async def middleware(request):
        resp = await handler(request)
        resp.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ', '.join([
                'PATCH', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
            'Access-Control-Allow-Headers': 'Content-Type',
        })
        return resp
    return middleware
