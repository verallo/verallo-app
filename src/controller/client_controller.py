from aiohttp import web
from src.service.accounts import bank_account_data, bank_account_data_from_all_sources
from src.service.auth import create_and_authenticate_client, refresh_auth_token, \
    add_new_account_to_existing_client_and_authenticate
from src.model.token import AuthTokenRequestPayload

routes = web.RouteTableDef()


@routes.post('/api/v1/token/create')
async def authenticate(request: web.Request) -> web.json_response:
    auth_request = await request.json()
    if auth_request['client_secret'] is None or auth_request['code'] is None:
        raise ValueError(f'One or more arguments do not exist. auth_request: {auth_request}')

    auth_response = await create_and_authenticate_client(
        AuthTokenRequestPayload(auth_request['client_secret'], auth_request['code']))
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/add')
async def add(request: web.Request) -> web.json_response:
    auth_request = await request.json()
    if auth_request['client_secret'] is None or auth_request['code'] is None or auth_request['client_uid'] is None:
        raise ValueError(f'One or more arguments do not exist. auth_request: {auth_request}')

    auth_response = await add_new_account_to_existing_client_and_authenticate(
        AuthTokenRequestPayload(auth_request['client_secret'], auth_request['code']), auth_request['client_uid'])
    return web.json_response(auth_response.__dict__)


@routes.post('/api/v1/token/refresh')
async def refresh(request: web.Request) -> web.json_response:
    account_uid = await request.json()
    if account_uid['account_uid'] is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {account_uid}')

    refresh_token_response = await refresh_auth_token(account_uid['account_uid'])
    return web.json_response(refresh_token_response.__dict__)


@routes.get('/api/v1/client/{client_uid}/accounts/{account_uid}')
async def get_account_data_from_one_bank(request: web.Request) -> web.json_response:
    account_uid = request.match_info['account_uid']
    if account_uid is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {account_uid}')
    bank_accounts_dict = await bank_account_data(account_uid)
    return web.json_response(bank_accounts_dict)


@routes.get('/api/v1/client/{client_uid}/accounts')
async def get_account_data_from_all_banks(request: web.Request) -> web.json_response:
    client_uid = request.match_info['client_uid']
    if client_uid is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {client_uid}')
    all_bank_accounts_dict = await bank_account_data_from_all_sources(client_uid)
    return web.json_response(all_bank_accounts_dict)


app = web.Application()
app.add_routes(routes)
web.run_app(app)
