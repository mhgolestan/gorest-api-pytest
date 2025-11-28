from http import HTTPStatus
import os

import allure
import pytest

from base.api.todos_api import TodosClient
from models.todos import (DefaultTodo, DefaultTodosList,
                              TodoDict, UpdateTodo)
from models.users import DefaultUser
from utils.assertions.api.todos import assert_todo
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema


@pytest.mark.todos
@allure.feature('Todos')
class TestTodos:

    @allure.story('Get Todos')
    @allure.title('Get todos list for user')
    def test_get_todos(self, class_todos_client: TodosClient):
        response = class_todos_client.get_all_todos_api()
        json_response: list[TodoDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultTodosList.model_json_schema())
    
    @allure.story('Get Todos')
    @allure.title('Get all todos for user')
    def test_get_user_todos(self, 
                            function_user: DefaultUser,
                            class_todos_client: TodosClient):        
        
        payload = UpdateTodo()
        class_todos_client.create_todo_api(function_user.id, payload)
        
        response = class_todos_client.get_todos_api(function_user.id)
        json_response: list[TodoDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultTodosList.model_json_schema())
    
    @allure.story('Create Todos')
    @allure.title('Create todo for user')
    def test_create_todo(self, 
                        function_user: DefaultUser,
                        class_todos_client: TodosClient):
        payload = UpdateTodo()
        response = class_todos_client.create_todo_api(function_user.id, payload)
        json_response: TodoDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        validate_schema(json_response, DefaultTodo.model_json_schema())   

    @allure.story('Create Todos')
    @allure.title('Create a user todo - negative test - missing required fields')
    @pytest.mark.parametrize(
        "todo_payload,expected_status", [
        ({"title": "Test Todo"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"due_on": "2024-12-31T23:59:59.000+05:30"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"status": "pending"}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ])
    def test_create_todo_negative(self,
                         function_user: DefaultUser,
                         class_todos_client: TodosClient,
                         todo_payload: dict,
                         expected_status: HTTPStatus):
        
        response = class_todos_client.create_todo_api_raw(function_user.id, todo_payload)

        assert_status_code(response.status_code, expected_status) 


    

    

