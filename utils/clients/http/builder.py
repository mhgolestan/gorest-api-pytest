from enum import Enum

from base.api.authentication_api import AuthenticationClient
from models.authentication import Authentication
from settings import base_settings
from utils.clients.http.client import HTTPClient


class AuthMethod(Enum):
    """Authentication method types supported by the API."""
    BEARER_TOKEN = "bearer_token"
    QUERY_PARAM = "query_param"


def get_http_client(
    auth: Authentication | None = None,
    base_url: str = base_settings.api_url,
    auth_method: AuthMethod = AuthMethod.BEARER_TOKEN
) -> HTTPClient:
    if auth is None:
        return HTTPClient(base_url=base_url, trust_env=True)

    headers: dict[str, str] = {}
    params: dict[str, str] = {}

    if auth_method == AuthMethod.BEARER_TOKEN:
        headers = {**headers, 'Authorization': f'Bearer {auth.user.token}'}
        return HTTPClient(base_url=base_url, headers=headers, trust_env=True)
    
    elif auth_method == AuthMethod.QUERY_PARAM:
        params = {'access_token': auth.user.token}
        return HTTPClient(base_url=base_url, params=params, trust_env=True)

    return HTTPClient(base_url=base_url, headers=headers, trust_env=True)