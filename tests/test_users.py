from http import HTTPStatus

import allure
import pytest

from base.api.users_api import UsersClient 
from models.users import (DefaultUser, DefaultUsersList,
                              UserDict, UpdateUser)
from utils.assertions.api.users import assert_user
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema


@pytest.mark.users
@allure.feature('Users')
@allure.story('Users API')
class TestUsers:
    @allure.title('Get users')
    def test_get_users(self, class_users_client: UsersClient):
        response = class_users_client.get_users_api()
        json_response: list[UserDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)

        validate_schema(
            json_response, DefaultUsersList.model_json_schema())

    @allure.title('Create user')
    def test_create_user(self, class_users_client: UsersClient):
        payload = DefaultUser()
        response = class_users_client.create_user_api(payload)
        json_response: UserDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_user(
            expected_user=json_response,
            actual_user=payload
        )

        validate_schema(json_response, DefaultUser.model_json_schema())