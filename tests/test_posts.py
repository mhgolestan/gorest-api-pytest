from http import HTTPStatus

import allure
import pytest

from base.api.posts_api import PostsClient 
from models.posts import (DefaultPost, DefaultPostsList,
                              PostDict, UpdatePost)
from models.users import DefaultUser
from utils.assertions.api.posts import assert_post
from utils.assertions.base.solutions import assert_status_code
from utils.assertions.schema import validate_schema


@pytest.mark.posts
@allure.feature('Posts')
class TestPosts:

    @allure.story('Get Posts')
    @allure.title('Get posts list for user')
    def test_get_posts(self, class_posts_client: PostsClient):
        response = class_posts_client.get_all_posts_api()
        json_response: list[PostDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultPostsList.model_json_schema())
    
    @allure.story('Get Posts')
    @allure.title('Get all posts for user')
    def test_get_user_posts(self, 
                            function_user: DefaultUser,
                            class_posts_client: PostsClient):        
        
        payload = UpdatePost()
        class_posts_client.create_post_api(function_user.id, payload)
        
        response = class_posts_client.get_posts_api(function_user.id)
        json_response: list[PostDict] = response.json()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_schema(json_response, DefaultPostsList.model_json_schema())
    
    @allure.story('Create Posts')
    @allure.title("Create a user's post")
    def test_create_post_positive(self, 
                         function_user: DefaultUser,
                         class_posts_client: PostsClient):
        
        payload = UpdatePost()
        response = class_posts_client.create_post_api(function_user.id, payload)
        json_response: PostDict = response.json()

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        validate_schema(json_response, DefaultPost.model_json_schema())
    
    @allure.story('Create Posts')
    @allure.title('Create a user post - negative test - missing required fields')
    @pytest.mark.parametrize(
        "post_payload,expected_status", [
        ({"title": "Test Post"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"body": "Test Body"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ])
    def test_create_post_negative(self, 
                         function_user: DefaultUser,
                         class_posts_client: PostsClient,
                         post_payload: dict,
                         expected_status: HTTPStatus):

        response = class_posts_client.create_post_api_raw(function_user.id, post_payload)

        assert_status_code(response.status_code, expected_status)
    
    



    

    

