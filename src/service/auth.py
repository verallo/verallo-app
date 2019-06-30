from src.model.token import AuthTokenResponsePayload, AuthTokenRefreshPayload
from src.client.client import post
from src.repository.auth_repository import create_new_client, save_client_access_token, select, \
    select_tokens_to_refresh, update_client_token
import json
import uuid

auth_url = 'https://auth.truelayer.com/connect/token'


async def authenticate_client(client) -> AuthTokenResponsePayload:
    # record the new client in the database
    client_uid = uuid.uuid4()
    await create_new_client(client_uid, 'ACTIVE')
    # send a request to true  layer
    response_payload = await post(auth_url, client.__dict__)
    auth_token_response_payload = AuthTokenResponsePayload(
        response_payload['access_token'],
        response_payload['expires_in'],
        response_payload['token_type'],
        response_payload['refresh_token'],
    )
    account_uid = uuid.uuid4()
    # save the access token in db
    await save_client_access_token(
        account_uid,
        client_uid,
        auth_token_response_payload.access_token,
        auth_token_response_payload.refresh_token
    )
    return auth_token_response_payload


async def refresh_auth_token(account_id: uuid.uuid4) -> AuthTokenResponsePayload:
    db_records = await select_tokens_to_refresh(account_id)
    db_record = db_records.pop(0)  # get first element from the list
    if db_record is None:
        raise ValueError('cant update non existing token')

    auth_refresh_token_payload = AuthTokenRefreshPayload(db_record['refresh_token'])
    response_payload = await post(auth_url, auth_refresh_token_payload.__dict__)
    token = AuthTokenResponsePayload(
        response_payload['access_token'],
        response_payload['expires_in'],
        response_payload['token_type'],
        response_payload['refresh_token'])

    await update_client_token(db_record['account_uid'], token)
    return token

