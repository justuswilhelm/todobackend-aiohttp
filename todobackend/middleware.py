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
