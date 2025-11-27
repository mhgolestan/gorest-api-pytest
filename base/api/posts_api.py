import allure
from httpx import Response

from models.posts import DefaultPost, UpdatePost
from utils.clients.http.client import APIClient
from utils.constants.routes import APIRoutes


class PostsClient(APIClient):
    @allure.step('Getting all posts')
    def get_all_posts_api(self) -> Response:
        return self.client.get(APIRoutes.POSTS)
    
    @allure.step('Getting all posts for user "{user_id}"')
    def get_posts_api(self, user_id: int) -> Response:
        return self.client.get(f'{APIRoutes.USERS}/{user_id}/posts')

    @allure.step('Creating post for user "{user_id}"')
    def create_post_api(self, user_id: int, payload: DefaultPost) -> Response:
        return self.client.post(f'{APIRoutes.USERS}/{user_id}/posts', json=payload.model_dump(by_alias=True))
    
    @allure.step('Creating post for user "{user_id}" with raw payload')
    def create_post_api_raw(self, user_id: int, payload: dict) -> Response:
        return self.client.post(f'{APIRoutes.USERS}/{user_id}/posts', json=payload)    

    def create_post(self, user_id: int) -> DefaultPost:
        payload = DefaultPost()
        response = self.create_post_api(user_id, payload)
        return DefaultPost(**response.json())