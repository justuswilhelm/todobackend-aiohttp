from os import environ
from json import dumps
from uuid import uuid4

from aiohttp import web
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPMethodNotAllowed,
)

db = {}
PORT = environ['PORT']


def get_object(request):
    uuid = request.match_info.get('uuid')
    try:
        return db[uuid]
    except KeyError:
        raise HTTPNotFound()


def delete_object(request):
    obj = get_object(request)
    del db[obj['uuid']]


class View:
    @classmethod
    async def dispatch(cls, request):
        method = getattr(cls, request.method.lower())

        if not method:
            return HTTPMethodNotAllowed()

        return await method(request)

    async def options(request):
        return web.Response(body=b'')


class IndexView(View):
    async def get(request):
        return web.Response(body=dumps(list(db.values())).encode())

    async def post(request):
        content = await request.json()
        uuid = str(uuid4())
        content['uuid'] = uuid
        content['completed'] = False
        content['url'] = 'http://localhost:{}/{}'.format(PORT, uuid)
        db[uuid] = content
        return web.Response(body=dumps(content).encode())

    async def put(request):
        return web.Response(body=b'')

    async def delete(request):
        global db
        db = {}
        return web.Response(body=b'')


class TodoView(View):
    async def get(request):
        obj = get_object(request)
        return web.Response(body=dumps(obj).encode())

    async def patch(request):
        obj = get_object(request)

        content = await request.json()
        obj.update(content)

        return web.Response(body=dumps(obj).encode())

    async def delete(request):
        delete_object(request)
        return web.Response(body=b'')
