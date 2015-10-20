from os import environ
from json import dumps
from uuid import uuid4

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .models import Task

PORT = environ['PORT']


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
        return web.Response(body=dumps(
            Task.all_objects()
        ).encode())

    async def post(request):
        content = await request.json()
        uuid = str(uuid4())
        content['uuid'] = uuid
        content['completed'] = False
        content['url'] = 'http://localhost:{}/{}'.format(PORT, uuid)
        Task.set_object(uuid, content)
        return web.Response(body=dumps(content).encode())

    async def put(request):
        return web.Response(body=b'')

    async def delete(request):
        Task.delete_all_objects()
        return web.Response(body=b'')


class TodoView(View):
    async def get(request):
        uuid = request.match_info.get('uuid')
        obj = Task.get_object(uuid)
        return web.Response(body=dumps(obj).encode())

    async def patch(request):
        uuid = request.match_info.get('uuid')
        obj = Task.get_object(uuid)

        content = await request.json()
        obj.update(content)

        return web.Response(body=dumps(obj).encode())

    async def delete(request):
        uuid = request.match_info.get('uuid')
        Task.delete_object(uuid)
        return web.Response(body=b'')
