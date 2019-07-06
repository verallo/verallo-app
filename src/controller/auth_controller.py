from aiohttp import web
from src.service.auth import create_and_authenticate_client, refresh_auth_token, \
    add_new_account_to_existing_client_and_authenticate
from src.model.token import AuthTokenRequestPayload

routes = web.RouteTableDef()


@routes.post('/api/v1/token/create')
async def authenticate(request: web.Request) -> web.json_response:
    auth_request = await request.json()
    if auth_request['code'] is None:
        raise ValueError(f'One or more arguments do not exist. auth_request: {auth_request}')
    auth_response = await create_and_authenticate_client(auth_request)
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/add')
async def add(request: web.Request) -> web.json_response:
    auth_request = await request.json()
    if auth_request['code'] is None or auth_request['client_uid'] is None:
        raise ValueError(f'One or more arguments do not exist. auth_request: {auth_request}')
    auth_response = await add_new_account_to_existing_client_and_authenticate(auth_request)
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/refresh')
async def refresh(request: web.Request) -> web.json_response:
    account_uid = await request.json()
    if account_uid['account_uid'] is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {account_uid}')
    refresh_token_response = await refresh_auth_token(account_uid['account_uid'])
    return web.json_response(refresh_token_response.__dict__)
