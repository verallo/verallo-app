from aiohttp import web

from src.service.transactions import transactions_from_one_bank, transactions_from_all_banks

routes = web.RouteTableDef()


@routes.get('/api/v1/client/{client_uid}/transactions/{account_uid}')
async def get_transactions_for_one_account(request: web.Request) -> web.json_response:
    account_uid = request.match_info['account_uid']
    if account_uid is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {account_uid}')
    transaction_dict = await transactions_from_one_bank(account_uid)
    return web.json_response(transaction_dict)


@routes.get('/api/v1/client/{client_uid}/transactions')
async def get_transactions_for_all_accounts(request: web.Request) -> web.json_response:
    client_uid = request.match_info['client_uid']
    if client_uid is None:
        raise ValueError(f'One or more arguments is does not exist. account_uid: {client_uid}')
    all_bank_balances_dict = await transactions_from_all_banks(client_uid)
    return web.json_response(all_bank_balances_dict)
