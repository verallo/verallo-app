from attr import dataclass


@dataclass(frozen=True)
class AuthTokenRequestPayload:
    client_id: str
    client_secret: str
    code: str
    grant_type: str = 'authorization_code'
    redirect_uri: str = 'https://console.truelayer.com/redirect-page'


@dataclass(frozen=True)
class AuthTokenResponsePayload:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str


@dataclass(frozen=True)
class AuthTokenRefreshPayload:
    client_id: str
    client_secret: str
    refresh_token: str
    grant_type: str = 'refresh_token'


@dataclass(frozen=True)
class AppCredentials:
    client_id: str
    client_secret: str
