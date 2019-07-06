from aiohttp import web
from src.service.accounts import bank_account_data, bank_account_data_from_all_sources

routes = web.RouteTableDef()


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
