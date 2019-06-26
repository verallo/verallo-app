import asyncpg
import uuid


async def create_connection_pool():
    return await asyncpg.create_pool(
        database='auth_app',
        user='true_layer_app',
        host='127.0.0.1',
        port=5432
    )


async def database_create_app_user(pool, *args) -> None:
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
           cats = await connection.execute(
               """ INSERT INTO authentication.app(app_uid, client_id, client_secret) VALUES ($1, $2, $3);""", *args
           )
        await connection.close()


async def create_new_client(pool, *args) -> uuid.uuid4:
    client_uid = uuid.uuid4()

    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                """ INSERT INTO authentication.client(client_uid, client_status) VALUES ($1, $2); """, *args)
        await connection.close()
    return client_uid


async def save_client_access_token(pool, *args) -> uuid.uuid4:
    account_uid = uuid.uuid4()
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                """ INSERT INTO authentication.account(account_uid, client_uid, access_token, refresh_token) 
                VALUES ($1, $2, $3, $4)""", account_uid, *args)
        await connection.close()
    return account_uid


async def select(pool, query, *args) -> list:
    async with pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetch(query, *args)
        await connection.close()
    return result


async def execute(pool, query, *args) -> None:
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(query, *args)
        await connection.close()

