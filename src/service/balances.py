import asyncio
import uuid
from src.client.client_api import get
from src.repository.auth_repository import select_auth_token, select_all_client_accounts
from src.service.accounts import bank_account_data

accounts_endpoint = 'https://api.truelayer.com/data/v1/accounts'


async def balance_from_one_bank(account_uid: uuid.uuid4) -> dict:
    # get all accounts
    results_dict = await bank_account_data(account_uid)
    bank_accounts_list = results_dict['results']
    #  TODO: get the token again (this is shitty) deal with it later
    db_records = await select_auth_token(account_uid)
    if db_records is None:
        raise Exception(f'auth token for account {account_uid} does not exist')
    token = db_records[0]['access_token']
    tasks = [get(url=f'{accounts_endpoint}/{account["account_id"]}/balance',
                 headers={'Authorization': f'Bearer {token}'})
             for account in bank_accounts_list]
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    return {str(account_uid): task_results}


async def balance_from_all_banks(client_uid: uuid.uuid4) -> dict:
    db_records = await select_all_client_accounts(client_uid)
    tasks = []
    for db_record in db_records:
        tasks.append(balance_from_one_bank(db_record['account_uid']))
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    return {'all_bank_accounts_balance': task_results}
