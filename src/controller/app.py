from aiohttp import web
from src.service.auth import authenticate_client, refresh_auth_token
from src.model.token import AuthTokenRequestPayload

routes = web.RouteTableDef()


@routes.post('/api/v1/token/create')
async def authenticate(request: web.Request) -> web.json_response:
    ap = await request.json()
    if ap['client_secret'] is None or ap['code'] is None:
        raise ValueError(f'One or more arguments do not exist: {ap}')

    auth_response = await authenticate_client(AuthTokenRequestPayload(ap['client_secret'], ap['code']))
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/refresh')
async def refresh(request: web.Request) -> web.json_response:
    account_uid = await request.json()
    if account_uid['account_uid'] is None:
        raise ValueError(f'One or more arguments is does not exist: {account_uid}')

    refresh_token_response = await refresh_auth_token(account_uid['account_uid'])
    return web.json_response(refresh_token_response.__dict__)


@routes.get('/api/v1/accounts/{account_uid}')
async def get_account_details(request: web.Request) -> web.json_response:
    pass


app = web.Application()
app.add_routes(routes)
web.run_app(app)
