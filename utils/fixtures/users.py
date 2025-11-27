import pytest

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