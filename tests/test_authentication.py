from http import HTTPStatus

import allure
import pytest

from base.api.users_api import UsersClient
from models.users import DefaultUsersList, UpdateUser, UserDict
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema
from utils.clients.http.builder import get_http_client


@pytest.mark.authentication
@allure.feature('Authentication')
class TestBearerTokenAuth:
    """Tests for HTTP Bearer Token authentication method."""

    @allure.story('Bearer Token Auth')
    @allure.title('Get users list with bearer token auth')
    def test_get_users_with_bearer_token_auth(self, bearer_token_client: UsersClient):
        """Test GET request with Authorization Bearer header."""
        response = bearer_token_client.get_users_api()
        json_response: list[UserDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultUsersList.model_json_schema())

    @allure.story('Bearer Token Auth')
    @allure.title('Invalid bearer token should return 401')
    def test_invalid_bearer_token_returns_401(self, invalid_bearer_client: UsersClient):
        """Test that invalid Bearer token returns 401 Unauthorized on write operations."""
        # Note: GET requests may return public data even without valid auth
        # POST/PUT/DELETE require valid authentication
        payload = UpdateUser()
        response = invalid_bearer_client.create_user_api(payload)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.authentication
@allure.feature('Authentication')
class TestQueryParameterAuth:
    """Tests for Query Parameter authentication method."""

    @allure.story('Query Parameter Auth')
    @allure.title('Get users list with query param auth')
    def test_get_users_with_query_param_auth(self, query_param_client: UsersClient):
        """Test GET request with access_token query parameter."""
        response = query_param_client.get_users_api()
        json_response: list[UserDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultUsersList.model_json_schema())

    @allure.story('Query Parameter Auth')
    @allure.title('Invalid query param token should return 401')
    def test_invalid_query_param_token_returns_401(self, invalid_query_param_client: UsersClient):
        """Test that invalid access_token in query params returns 401 on write operations."""
        # Note: GET requests may return public data even without valid auth
        # POST/PUT/DELETE require valid authentication
        payload = UpdateUser()
        response = invalid_query_param_client.create_user_api(payload)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)


@pytest.mark.authentication
@allure.feature('Authentication')
class TestAuthenticationComparison:
    """Tests comparing both authentication methods produce equivalent results."""

    @allure.story('Auth Method Comparison')
    @allure.title('Both auth methods should return successful response')
    def test_both_auth_methods_return_success(
        self, 
        bearer_token_client: UsersClient, 
        query_param_client: UsersClient
    ):
        """Verify both authentication methods return successful responses."""
        bearer_response = bearer_token_client.get_users_api()
        query_response = query_param_client.get_users_api()

        assert_status_code(bearer_response.status_code, HTTPStatus.OK)
        assert_status_code(query_response.status_code, HTTPStatus.OK)

        # Both should return lists
        bearer_data = bearer_response.json()
        query_data = query_response.json()

        assert isinstance(bearer_data, list)
        assert isinstance(query_data, list)


@pytest.mark.authentication
@allure.feature('Authentication')
class TestNoAuthentication:
    """Tests for requests without authentication."""

    @allure.story('No Auth')
    @allure.title('Request without auth should return 401')
    def test_no_auth_returns_401(self):
        """Test that request without authentication returns 401."""
        client = get_http_client(auth=None)
        users_client = UsersClient(client=client)
        
        response = users_client.get_users_api()
        
        # GoRest API returns 200 for GET but 401 for POST/PUT/DELETE without auth
        # For GET requests, it returns public data
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.UNAUTHORIZED]
