import allure
from httpx import Response

from models.users import DefaultUser, UpdateUser 
from utils.clients.http.client import APIClient
from utils.constants.routes import APIRoutes


class UsersClient(APIClient):
    @allure.step('Getting all users')
    def get_users_api(self) -> Response:
        return self.client.get(APIRoutes.USERS)

    @allure.step('Getting user with id "{user_id}"')
    def get_user_api(self, user_id: int) -> Response:
        return self.client.get(f'{APIRoutes.USERS}/{user_id}')

    @allure.step('Creating user')
    def create_user_api(self, payload: DefaultUser) -> Response:
        return self.client.post(APIRoutes.USERS, json=payload.model_dump(by_alias=True))

    @allure.step('Updating user with id "{user_id}"')
    def update_user_api(self, user_id: int, payload: UpdateUser) -> Response:
        return self.client.patch(
            f'{APIRoutes.USERS}/{user_id}',
            json=payload.model_dump(by_alias=True)
        )

    @allure.step('Deleting user with id "{user_id}"')
    def delete_user_api(self, user_id: int) -> Response:
        return self.client.delete(f'{APIRoutes.USERS}/{user_id}')

    def create_user(self) -> DefaultUser:
        payload = DefaultUser()
        response = self.create_user_api(payload)
        return DefaultUser(**response.json())