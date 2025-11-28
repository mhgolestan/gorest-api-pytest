import allure
from httpx import Response

from models.todos import DefaultTodo, UpdateTodo
from utils.clients.http.client import APIClient
from utils.constants.routes import APIRoutes


class TodosClient(APIClient):
    @allure.step('Getting all todos')
    def get_all_todos_api(self) -> Response:
        return self.client.get(APIRoutes.TODOS)
    
    @allure.step('Getting all todos for user "{user_id}"')
    def get_todos_api(self, user_id: int) -> Response:
        return self.client.get(f'{APIRoutes.USERS}/{user_id}/todos')

    @allure.step('Creating todo for user "{user_id}"')
    def create_todo_api(self, user_id: int, payload: UpdateTodo) -> Response:
        return self.client.post(f'{APIRoutes.USERS}/{user_id}/todos', json=payload.model_dump(by_alias=True))
    
    @allure.step('Creating todo for user "{user_id}" with raw payload')
    def create_todo_api_raw(self, user_id: int, payload: dict) -> Response:
        return self.client.post(f'{APIRoutes.USERS}/{user_id}/todos', json=payload)
    
    def create_todo(self, user_id: int) -> DefaultTodo:
        payload = UpdateTodo()
        response = self.create_todo_api(user_id, payload)
        return DefaultTodo(**response.json())