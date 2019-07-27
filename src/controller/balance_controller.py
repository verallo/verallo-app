from aiohttp import web
from src.service.balances import balance_from_one_bank, balance_from_all_banks
import logging
routes = web.RouteTableDef()


@routes.get('/api/v1/client/{client_uid}/balance/{account_uid}')
async def get_balance_for_one_account(request: web.Request) -> web.json_response:
    account_uid = request.match_info['account_uid']
    logging.info(f'getting account balance for: {account_uid}')
    if account_uid is None:
        logging.error(f'One or more arguments is does not exist. account_uid: {account_uid}')
        raise ValueError(f'One or more arguments is does not exist. account_uid: {account_uid}')
    balance_dict = await balance_from_one_bank(account_uid)
    return web.json_response(balance_dict)


@routes.get('/api/v1/client/{client_uid}/balance')
async def get_balance_for_all_accounts(request: web.Request) -> web.json_response:
    client_uid = request.match_info['client_uid']
    logging.info(f'getting account balance from all accounts for : {client_uid}')
    if client_uid is None:
        logging.error(f'One or more arguments is does not exist. account_uid: {client_uid}')
        raise ValueError(f'One or more arguments is does not exist. account_uid: {client_uid}')
    all_bank_balances_dict = await balance_from_all_banks(client_uid)
    return web.json_response(all_bank_balances_dict)
