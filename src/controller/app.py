from aiohttp import web
from src.service.auth import authenticate_client
from src.model.token import AuthTokenRequestPayload

routes = web.RouteTableDef()


@routes.post('/api/v1/token/create')
async def authenticate(request: web.Request) -> web.json_response:
    ap = await request.json()
    if (ap['client_id'] is None or
            ap['client_secret'] is None or
            ap['code'] is None or
            ap['redirect_uri'] is None or
            ap['grant_type'] == None):
        raise ValueError(f'One or more arguments is does not exist: {apj}')

    auth_response =  await authenticate_client(
        AuthTokenRequestPayload(
            ap['client_secret'],
            ap['code'],
            ap['grant_type'],
            ap['client_id'],
            ap['redirect_uri']
        )
    )
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/refresh')
async def refresh(request: web.Request) -> web.json_response:
    pass


app = web.Application()
app.add_routes(routes)
web.run_app(app)
