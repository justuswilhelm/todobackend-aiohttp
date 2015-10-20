from json import dumps
from logging import getLogger
from os import environ
from uuid import uuid4

from aiohttp.web import Response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .models import Task

logger = getLogger(__name__)
PORT = environ['PORT']


class JSONResponse(Response):
    def __init__(self, content):
        super().__init__(text=dumps(content))


class View:
    @classmethod
    async def dispatch(cls, request):
        method = getattr(cls, request.method.lower())
        logger.info(
            "Serving %s %s",
            request.method, request.path)

        if not method:
            return HTTPMethodNotAllowed()

        return await method(request)

    async def options(request):
        return Response()


class IndexView(View):
    async def get(request):
        return JSONResponse(Task.all_objects())

    async def post(request):
        content = await request.json()
        uuid = str(uuid4())
        content['uuid'] = uuid
        content['completed'] = False
        content['url'] = 'http://localhost:{}/{}'.format(PORT, uuid)
        Task.set_object(uuid, content)
        return JSONResponse(content)

    async def delete(request):
        Task.delete_all_objects()
        return Response()


class TodoView(View):
    async def get(request):
        uuid = request.match_info.get('uuid')
        obj = Task.get_object(uuid)
        return JSONResponse(obj)

    async def patch(request):
        uuid = request.match_info.get('uuid')
        obj = Task.get_object(uuid)

        content = await request.json()
        obj.update(content)

        return JSONResponse(obj)

    async def delete(request):
        uuid = request.match_info.get('uuid')
        Task.delete_object(uuid)
        return Response()
