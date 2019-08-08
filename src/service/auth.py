import logging

from src.model.token import AuthTokenResponsePayload, AuthTokenRefreshPayload, AuthTokenRequestPayload, AppCredentials
from src.client.client_api import post
from src.repository.auth_repository import create_new_client, save_client_access_token, \
    select_tokens_to_refresh, update_client_token, select_app_credentials, check_if_the_client_exist
import uuid

auth_url = 'https://auth.truelayer.com/connect/token'


async def create_and_authenticate_client(request_payload: dict) -> AuthTokenResponsePayload:
    # record the new client in the database
    client_uid = uuid.uuid4()
    await create_new_client(client_uid, 'ACTIVE')
    app_credentials = await select_app_credentials()
    auth_payload = AuthTokenRequestPayload(
        app_credentials.client_id, app_credentials.client_secret, request_payload['code'])
    # send a request to true  layer
    response_payload = await post(auth_url, auth_payload.__dict__)
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


async def add_new_account_to_existing_client_and_authenticate(request_payload: dict) -> AuthTokenResponsePayload:
    if await check_if_the_client_exist(request_payload['client_uid']):
        app_credentials = await select_app_credentials()
        auth_payload = AuthTokenRequestPayload(
            app_credentials.client_id, app_credentials.client_secret, request_payload['code'])
        # send a request to true layer
        response_payload = await post(auth_url, auth_payload.__dict__)
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
            request_payload['client_uid'],
            auth_token_response_payload.access_token,
            auth_token_response_payload.refresh_token
        )
    else:
        logging.error('selected client_uid does not exist in the system')
        raise ValueError('selected client_uid does not exist in the system')
    return auth_token_response_payload


async def refresh_auth_token(account_id: uuid.uuid4) -> AuthTokenResponsePayload:
    db_tokens = await select_tokens_to_refresh(account_id)
    app_credentials = await select_app_credentials()
    db_token = db_tokens.pop(0)  # get first element from the list
    if db_token is None:
        logging.error(f'token for account_uid {account_id} does not exist')
        raise TypeError(f'token for account_uid {account_id} does not exist')

    auth_refresh_token_payload = AuthTokenRefreshPayload(
        app_credentials.client_id, app_credentials.client_secret, db_token['refresh_token'])
    response_payload = await post(auth_url, auth_refresh_token_payload.__dict__)
    token = AuthTokenResponsePayload(
        response_payload['access_token'],
        response_payload['expires_in'],
        response_payload['token_type'],
        response_payload['refresh_token'])

    await update_client_token(db_token['account_uid'], token)
    return token
