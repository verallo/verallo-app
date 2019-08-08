import asyncio
import logging
import uuid
from src.client.client_api import get
from src.repository.auth_repository import select_auth_token, select_all_client_accounts, check_if_the_client_exist, \
    check_if_the_account_exist
from src.service.auth import refresh_auth_token

accounts_endpoint = 'https://api.truelayer.com/data/v1/accounts'


async def bank_account_data(account_uid: uuid.uuid4) -> dict:
    if await check_if_the_account_exist(account_uid):
        # refresh token
        await refresh_auth_token(account_uid)
        # get data from db
        db_records = await select_auth_token(account_uid)
        if db_records is None:
            logging.error(f'auth token for account {account_uid} does not exist')
            raise TypeError(f'auth token for account {account_uid} does not exist')
        token = db_records[0]['access_token']
        # get the account data
        results_dict = await get(url=accounts_endpoint, headers={'Authorization': f'Bearer {token}'})
    else:
        logging.error(f'selected account_uid: {account_uid} does not exist in the system')
        raise ValueError(f'selected account_uid: {account_uid} does not exist in the system')
    return results_dict


async def bank_account_data_from_all_sources(client_uid: uuid.uuid4) -> dict:
    if await check_if_the_client_exist(client_uid):
        db_records = await select_all_client_accounts(client_uid)
        tasks = []
        for db_record in db_records:
            tasks.append(bank_account_data(db_record['account_uid']))
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
    else:
        logging.error(f'selected client_uid: {client_uid} does not exist in the system')
        raise ValueError(f'selected client_uid: {client_uid} does not exist in the system')
    return {'all_bank_accounts': task_results}



