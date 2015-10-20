from json import dumps
from logging import getLogger

from aiohttp.web import Response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .models import Task

logger = getLogger(__name__)


class JSONResponse(Response):
    def __init__(self, content):
        super().__init__(text=dumps(content))


class View:
    @classmethod
    async def dispatch(cls, request):
        view = cls()
        method = getattr(view, request.method.lower())
        logger.info(
            "Serving %s %s",
            request.method, request.path)

        if not method:
            return HTTPMethodNotAllowed()

        return await method(request)

    @classmethod
    async def options(self, request):
        return Response()


class IndexView(View):
    async def get(self, request):
        return JSONResponse(Task.all_objects())

    async def post(self, request):
        content = await request.json()
        return JSONResponse(
            Task.create_object(content)
        )

    async def delete(self, request):
        Task.delete_all_objects()
        return Response()


class TodoView(View):
    async def get(self, request):
        uuid = request.match_info.get('uuid')
        return JSONResponse(Task.get_object(uuid))

    async def patch(self, request):
        uuid = request.match_info.get('uuid')
        content = await request.json()
        return JSONResponse(Task.update_object(uuid, content))

    async def delete(self, request):
        uuid = request.match_info.get('uuid')
        Task.delete_object(uuid)
        return Response()
