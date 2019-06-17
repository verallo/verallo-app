from aiohttp import web
from src.service.auth import authenticate_client, refresh_auth_token
from src.model.token import AuthTokenRequestPayload, AuthTokenRefreshPayload

routes = web.RouteTableDef()


@routes.post('/api/v1/token/create')
async def authenticate(request: web.Request) -> web.json_response:
    ap = await request.json()
    if (
            ap['client_id'] is None or
            ap['client_secret'] is None or
            ap['code'] is None or
            ap['redirect_uri'] is None or
            ap['grant_type'] is None
    ):
        raise ValueError(f'One or more arguments is does not exist: {apj}')

    auth_response = await authenticate_client(
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
    ref_pd = await request.json()
    if (
            ref_pd['client_id'] is None or
            ref_pd['client_secret'] is None or
            ref_pd['refresh_token'] is None or
            ref_pd['grant_type'] is None
    ):
        raise ValueError(f'One or more arguments is does not exist: {apj}')

    refresh_token_response = await refresh_auth_token(
        AuthTokenRefreshPayload(
            ref_pd['refresh_token'],
            ref_pd['client_secret'],
            ref_pd['client_id'],
            ref_pd['grant_type'],
        )
    )
    return web.json_response(refresh_token_response.__dict__)


app = web.Application()
app.add_routes(routes)
web.run_app(app)
