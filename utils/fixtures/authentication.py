import pytest

from base.api.users_api import UsersClient
from models.authentication import Authentication, AuthUser
from utils.clients.http.builder import AuthMethod, get_http_client


@pytest.fixture(scope="class")
def bearer_token_client() -> UsersClient:
    """Client using HTTP Bearer Token authentication."""
    client = get_http_client(
        auth=Authentication(),
        auth_method=AuthMethod.BEARER_TOKEN
    )
    return UsersClient(client=client)


@pytest.fixture(scope="class")
def query_param_client() -> UsersClient:
    """Client using Query Parameter authentication."""
    client = get_http_client(
        auth=Authentication(),
        auth_method=AuthMethod.QUERY_PARAM
    )
    return UsersClient(client=client)


@pytest.fixture(scope="function")
def invalid_bearer_client() -> UsersClient:
    """Client using invalid Bearer Token."""
    invalid_auth = Authentication(user=AuthUser(token="invalid_token_12345"))
    client = get_http_client(
        auth=invalid_auth,
        auth_method=AuthMethod.BEARER_TOKEN
    )
    return UsersClient(client=client)


@pytest.fixture(scope="function")
def invalid_query_param_client() -> UsersClient:
    """Client using invalid query parameter token."""
    invalid_auth = Authentication(user=AuthUser(token="invalid_token_12345"))
    client = get_http_client(
        auth=invalid_auth,
        auth_method=AuthMethod.QUERY_PARAM
    )
    return UsersClient(client=client)
