from src.model.token import AuthTokenRequestPayload
from src.model.token import AuthTokenResponsePayload
from src.client.client import post
import json


async def authenticate_client(client: AuthTokenRequestPayload) -> AuthTokenResponsePayload:
    auth_url: str = 'https://auth.truelayer.com/connect/token'
    status, response_payload = await post(auth_url, client.__dict__)
    if 200 <= status < 300:
        dr = json.loads(response_payload)
        return AuthTokenResponsePayload(
            dr['access_token'],
            dr['expires_in'],
            dr['token_type'],
            dr['refresh_token'],
        )
    else:
        raise Exception("Authentication failed")
