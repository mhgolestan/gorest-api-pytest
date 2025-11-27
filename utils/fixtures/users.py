import pytest
import time

from base.api.users_api import UsersClient
from models.authentication import Authentication
from models.users import DefaultUser
from utils.clients.http.builder import get_http_client
    

@pytest.fixture(scope="class")
def class_users_client() -> UsersClient:
    client = get_http_client(auth=Authentication())

    return UsersClient(client=client)

@pytest.fixture(scope='function')
def function_user(class_users_client: UsersClient) -> DefaultUser:
    user = class_users_client.create_user()
    yield user

    class_users_client.delete_user_api(user.id)

@pytest.fixture(autouse=True)
def rate_limit_delay():
    """Add delay between tests to avoid rate limiting"""
    yield
    time.sleep(0.5)