from attr import dataclass


@dataclass
class AuthTokenRequestPayload:
    client_secret: str
    code: str
    grant_type: str = 'authorization_code'
    client_id: str = 'meowmeowcat-041410'
    redirect_uri: str = 'https://console.truelayer.com/redirect-page'


@dataclass
class AuthTokenResponsePayload:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str


@dataclass
class AuthTokenRefreshPayload:
    refresh_token: str
    client_secret: str
    client_id: str = 'meowmeowcat-041410'
    grant_type: str = 'refresh_token'
