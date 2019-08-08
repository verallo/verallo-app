import asyncpg
import uuid

from src.model.token import AuthTokenResponsePayload, AppCredentials


async def create_connection_pool():
    return await asyncpg.create_pool(
        database='auth_app',
        user='true_layer_app',
        host='127.0.0.1',
        port=5432
    )


async def create_connection() -> asyncpg.Connection:
    return await asyncpg.connect(
        database='auth_app',
        user='true_layer_app',
        host='127.0.0.1',
        port=5432)


async def create_new_client(client_uid: uuid.uuid4, client_status: str) -> None:
    await execute(""" INSERT INTO authentication.client(client_uid, client_status) VALUES ($1, $2); """,
                  client_uid, client_status)


async def save_client_access_token(account_uid: uuid.uuid4, client_id: uuid.uuid4, access_token: str,
                                   refresh_token: str) -> None:
    await execute(""" INSERT INTO authentication.account(account_uid, client_uid, access_token, refresh_token) 
        VALUES ($1, $2, $3, $4)""", account_uid, client_id, access_token, refresh_token)


async def select_tokens_to_refresh(account_uid: uuid.uuid4) -> list:
    return await select(
        """ SELECT account_uid, access_token, refresh_token FROM authentication.account WHERE account_uid = $1 """,
        account_uid)


async def select_auth_token(account_uid: uuid.uuid4) -> list:
    return await select(
        """ SELECT access_token FROM authentication.account WHERE account_uid = $1 """, account_uid)


async def update_client_token(account_uid: uuid.uuid4, token: AuthTokenResponsePayload) -> None:
    await execute(""" UPDATE authentication.account SET access_token = $1, refresh_token = $2 WHERE account_uid = $3 """,
                  token.access_token, token.refresh_token, account_uid)


async def select_all_client_accounts(client_uid: uuid.uuid4) -> list:
    return await select(""" SELECT account_uid FROM authentication.account WHERE client_uid = $1 """, client_uid)


async def check_if_the_client_exist(client_uid: uuid.uuid4) -> bool:
    bool_list = await select(""" SELECT 1 FROM authentication.account WHERE client_uid = $1 """, client_uid)
    return False if not bool_list else True


async def check_if_the_account_exist(account_uid: uuid.uuid4) -> bool:
    bool_list = await select(""" SELECT 1 FROM authentication.account WHERE account_uid = $1 """, account_uid)
    return False if not bool_list else True


async def select_app_credentials() -> AppCredentials:
    db_records = await select(""" SELECT client_id, client_secret FROM authentication.app 
    WHERE app_uid = 'f3235a6e-1140-4c14-8350-aad2be7aee18' """)
    record = db_records[0]
    return AppCredentials(record['client_id'], record['client_secret'])


async def select(query, *args) -> list:
    connection = await create_connection()
    result = await connection.fetch(query, *args)
    await connection.close()
    return result


async def execute(query, *args) -> None:
    connection = await create_connection()
    await connection.execute(query, *args)
    await connection.close()
