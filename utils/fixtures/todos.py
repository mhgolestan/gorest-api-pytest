import pytest
import time

from base.api.todos_api import TodosClient
from models.authentication import Authentication
from models.todos import DefaultTodo
from models.users import DefaultUser
from utils.clients.http.builder import get_http_client
    

@pytest.fixture(scope="class")
def class_todos_client() -> TodosClient:
    client = get_http_client(auth=Authentication())

    return TodosClient(client=client)

@pytest.fixture(scope='function')
def function_todo(function_user: DefaultUser,
                  class_todos_client: TodosClient) -> DefaultTodo:

    user_id = function_user.id
    todo = class_todos_client.create_todo(user_id)
    yield todo

    class_todos_client.delete_todo_api(user_id, todo.id)

@pytest.fixture(autouse=True)
def rate_limit_delay():
    """Add delay between tests to avoid rate limiting"""
    yield
    time.sleep(0.5)