from logging import getLogger, basicConfig, INFO
from os import getenv
from aiohttp import web

from .middleware import cors_middleware_factory
from .views import (
    IndexView,
    TodoView,
)

IP = '0.0.0.0'
PORT = getenv('PORT', '8000')

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
