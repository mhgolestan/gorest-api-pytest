import pytest
import time

from base.api.posts_api import PostsClient
from models.authentication import Authentication
from models.posts import DefaultPost
from models.users import DefaultUser
from utils.clients.http.builder import get_http_client
    

@pytest.fixture(scope="class")
def class_posts_client() -> PostsClient:
    client = get_http_client(auth=Authentication())

    return PostsClient(client=client)

@pytest.fixture(scope='function')
def function_post(function_user: DefaultUser,
                  class_posts_client: PostsClient) -> DefaultPost:

    user_id = function_user.id
    post = class_posts_client.create_post(user_id)
    yield post

@pytest.fixture(autouse=True)
def rate_limit_delay():
    """Add delay between tests to avoid rate limiting"""
    yield
    time.sleep(0.5)