from os import environ
from json import dumps
from uuid import uuid4

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound

db = {}
PORT = environ['PORT']


class View:
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
        uuid = request.match_info.get('uuid')
        try:
            content = db[uuid]
            return web.Response(body=dumps(content).encode())
        except KeyError:
            return HTTPNotFound()

    async def patch(request):
        uuid = request.match_info.get('uuid')
        try:
            todo = db[uuid]
        except KeyError:
            return HTTPNotFound()

        content = await request.json()
        todo.update(content)
        return web.Response(body=dumps(todo).encode())

    async def delete(request):
        uuid = request.match_info.get('uuid')
        try:
            del db[uuid]
        except KeyError:
            return HTTPNotFound()
        return web.Response(body=b'')
