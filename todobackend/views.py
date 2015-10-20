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
    def __init__(self, request):
        self.request = request

    @classmethod
    async def dispatch(cls, request):
        view = cls(request)
        method = getattr(view, request.method.lower())
        logger.info(
            "Serving %s %s",
            request.method, request.path)

        if not method:
            return HTTPMethodNotAllowed()

        return await method()

    async def options(self):
        return Response()


class IndexView(View):
    async def get(self):
        return JSONResponse(Task.all_objects())

    async def post(self):
        content = await self.request.json()
        return JSONResponse(
            Task.create_object(content)
        )

    async def delete(self):
        Task.delete_all_objects()
        return Response()


class TodoView(View):
    def __init__(self, request):
        super().__init__(request)
        self.uuid = request.match_info.get('uuid')

    async def get(self):
        return JSONResponse(Task.get_object(self.uuid))

    async def patch(self):
        content = await self.request.json()
        return JSONResponse(
            Task.update_object(self.uuid, content))

    async def delete(self):
        Task.delete_object(self.uuid)
        return Response()
