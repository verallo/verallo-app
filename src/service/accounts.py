import asyncio
import uuid
from src.client.client_api import get
from src.repository.auth_repository import select_auth_token, select_all_client_accounts
from src.service.auth import refresh_auth_token

accounts_endpoint = 'https://api.truelayer.com/data/v1/accounts'


async def bank_account_data(account_uid: uuid.uuid4) -> dict:
    # refresh token
    await refresh_auth_token(account_uid)
    # get data from db
    db_records = await select_auth_token(account_uid)
    if db_records is None:
        raise TypeError(f'auth token for account {account_uid} does not exist')
    token = db_records[0]['access_token']
    # get the account data
    results_dict = await get(url=accounts_endpoint, headers={'Authorization': f'Bearer {token}'})
    return results_dict


async def bank_account_data_from_all_sources(client_uid: uuid.uuid4) -> dict:
    db_records = await select_all_client_accounts(client_uid)
    tasks = []
    for db_record in db_records:
        tasks.append(bank_account_data(db_record['account_uid']))
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    return {'all_bank_accounts': task_results}



