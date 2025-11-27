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
class TestUsers:

    @allure.story('Get Users')
    @allure.title('Get users list')
    def test_get_users(self, class_users_client: UsersClient):
        response = class_users_client.get_users_api()
        json_response: list[UserDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)

        validate_schema(
            json_response, DefaultUsersList.model_json_schema())

    @allure.story('Create user')
    @allure.title('Create user - positive')
    def test_create_user(self, class_users_client: UsersClient):
        payload = UpdateUser()
        response = class_users_client.create_user_api(payload)
        json_response: UserDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_user(
            expected_user=json_response,
            actual_user=payload
        )

        validate_schema(json_response, DefaultUser.model_json_schema())
    
    @allure.story('Create user')
    @allure.title('Create user - negative')
    @pytest.mark.parametrize("payload,expected_status", [
        ({"name": 12345, "email": "invalid-email"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"email": "test@example.com"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ])
    def test_create_user_invalid_payload(self, 
                                         class_users_client: UsersClient,
                                         payload: dict,
                                         expected_status: HTTPStatus):
        response = class_users_client.create_user_api_raw(payload) 
        assert_status_code(response.status_code, expected_status)

    @allure.story('Get User by ID')
    @allure.title('Get user by ID - positive')
    def test_get_user_by_id_success(self, 
                                    class_users_client: UsersClient, 
                                    function_user: DefaultUser):
        response = class_users_client.get_user_api(function_user.id)
        json_response: UserDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert json_response['id'] == function_user.id
        validate_schema(json_response, DefaultUser.model_json_schema())
    
    @allure.story('Get User by ID')
    @allure.title('Get user by ID - user not found')
    @pytest.mark.parametrize("user_id", [999999, -1, 0])
    def test_get_user_by_id_not_found(self, 
                                      class_users_client: UsersClient,
                                      user_id: int):
        response = class_users_client.get_user_api(user_id)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert response.json()['message'] == 'Resource not found'
    
    @allure.story('Update User')
    @allure.title('Update user - positive')
    def test_update_user(
        self,
        function_user: DefaultUser,
        class_users_client: UsersClient
    ):
        payload = UpdateUser()

        response = class_users_client.update_user_api(
            function_user.id, payload
        )
        json_response: UserDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_user(
            expected_user=json_response,
            actual_user=payload
        )
        validate_schema(json_response, DefaultUser.model_json_schema())
    
    @allure.story('Update User')
    @allure.title('Update user - user not found')
    @pytest.mark.parametrize("user_id", [999999, -1, 0])
    def test_update_user_not_found(self, 
                                   class_users_client: UsersClient,
                                   user_id: int):
        payload = UpdateUser(name="Updated Name")
        response = class_users_client.update_user_api(user_id, payload)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert response.json()['message'] == 'Resource not found'
    
    @allure.story('Delete User')
    @allure.title('Delete user - positive')
    def test_delete_user(
        self,
        function_user: DefaultUser,
        class_users_client: UsersClient
    ):
        delete_user_response = class_users_client.delete_user_api(
            function_user.id
        )
        get_user_response = class_users_client.get_user_api(
            function_user.id
        )

        assert_status_code(delete_user_response.status_code, HTTPStatus.NO_CONTENT)
        assert_status_code(
            get_user_response.status_code, HTTPStatus.NOT_FOUND
        )
    
    @allure.story('Delete User')
    @allure.title('Delete updated user')
    def test_delete_updated_user(
        self,
        function_user: DefaultUser,
        class_users_client: UsersClient
    ):
        # Update the user first
        update_payload = UpdateUser()
        update_response = class_users_client.update_user_api(function_user.id, update_payload)
        assert_status_code(update_response.status_code, HTTPStatus.OK)
        
        updated_user = update_response.json()
        assert_user(
            expected_user=updated_user,
            actual_user=update_payload
        )
        validate_schema(updated_user, DefaultUser.model_json_schema())
        
        # Delete the updated user
        delete_response = class_users_client.delete_user_api(function_user.id)
        assert_status_code(delete_response.status_code, HTTPStatus.NO_CONTENT)
        
        # Verify user is deleted
        get_response = class_users_client.get_user_api(function_user.id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
    
    @allure.story('Delete User')
    @allure.title('Delete user - user not found')
    @pytest.mark.parametrize("user_id", [999999, -1, 0])
    def test_delete_user_not_found(self, 
                                   class_users_client: UsersClient,
                                   user_id: int):
        response = class_users_client.delete_user_api(user_id)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert response.json()['message'] == 'Resource not found'

    @allure.story('Create user')
    @allure.title('Create user with overflow payload')
    @pytest.mark.parametrize("overflow_size,field_name", [
        (10000, "name"),
        (10000, "email"),
        (100000, "name"),
    ])
    def test_create_user_overflow(self, 
                                  class_users_client: UsersClient,
                                  overflow_size: int,
                                  field_name: str):
        payload_dict = {
            "name": "x" * overflow_size if field_name == "name" else "Test User",
            "email": "x" * overflow_size + "@example.com" if field_name == "email" else "test@example.com"
        }
        response = class_users_client.create_user_api_raw(payload_dict)
        
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    @allure.story('Update user')
    @allure.title('Update user with overflow payload')
    @pytest.mark.parametrize("overflow_size,field_name", [
        (10000, "name"),
        (100000, "name"),
    ])
    def test_update_user_overflow(self, 
                                  function_user: DefaultUser,
                                  class_users_client: UsersClient,
                                  overflow_size: int,
                                  field_name: str):
        payload = UpdateUser(name="x" * overflow_size if field_name == "name" else "Updated")
        response = class_users_client.update_user_api(function_user.id, payload)
        
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
    
    @allure.story('Create user')
    @allure.title('Create user with SQL injection attempt')
    @pytest.mark.parametrize("sql_injection_payload", [
        {"name": "'; DROP TABLE users; --", "email": "test@example.com"},
        {"name": "Test' OR '1'='1", "email": "test@example.com"},
        {"name": "Test", "email": "test@example.com' OR '1'='1"},
        {"name": "Test\"; DROP TABLE users; //", "email": "test@example.com"},
        {"name": "Test", "email": "admin'--"},
        {"name": "Test", "email": "' UNION SELECT * FROM users--"},
        {"name": "Test", "email": "test@example.com'; DELETE FROM users; --"},
        {"name": "Test", "email": "test@example.com' AND 1=1"},
        {"name": "Test", "email": "test@example.com' AND SLEEP(5)--"},
    ])
    def test_create_user_sql_injection(self, 
                                       class_users_client: UsersClient,
                                       sql_injection_payload: dict):
        response = class_users_client.create_user_api_raw(sql_injection_payload)
        
        # Should either reject or safely handle the payload
        assert response.status_code in [HTTPStatus.CREATED, HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.BAD_REQUEST]
        
        # Verify table still exists and data integrity is maintained
        get_response = class_users_client.get_users_api()
        assert_status_code(get_response.status_code, HTTPStatus.OK)

    @allure.story('Update user')
    @allure.title('Update user with SQL injection attempt')
    @pytest.mark.parametrize("sql_injection_payload", [
        {"name": "'; DROP TABLE users; --"},
        {"name": "Test' OR '1'='1"},
        {"name": "Test\"; DROP TABLE users; //"},
        {"name": "admin'--"},
    ])
    def test_update_user_sql_injection(self, 
                                       function_user: DefaultUser,
                                       class_users_client: UsersClient,
                                       sql_injection_payload: dict):
        response = class_users_client.create_user_api_raw(sql_injection_payload)
        
        # Should either reject or safely handle the payload
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.BAD_REQUEST]
        
        # Verify original user still exists
        get_response = class_users_client.get_user_api(function_user.id)
        assert_status_code(get_response.status_code, HTTPStatus.OK)

    @pytest.mark.parametrize("sql_injection_user_id", [
        "1'; DROP TABLE users; --",
        "1 OR 1=1",
        "1 UNION SELECT * FROM users",
        "1; DELETE FROM users WHERE 1=1; --",
    ])
    @allure.story('Get user by ID')
    @allure.title('Get user with SQL injection in ID')
    def test_get_user_sql_injection_id(self, 
                                       class_users_client: UsersClient,
                                       sql_injection_user_id: str):

        response = class_users_client.get_user_api(sql_injection_user_id)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
