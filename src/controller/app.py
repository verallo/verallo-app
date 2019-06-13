from aiohttp import web


routes = web.RouteTableDef()

@routes.get('/api/v1/finacials/{id}')
async def handler(request: web.Request) -> web.json_response:
    data = request.match_info['id']
    return web.json_response({'code': 200, 'data': data})

app = web.Application()
app.add_routes(routes)
web.run_app(app)