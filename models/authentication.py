from pydantic import BaseModel, Field, model_validator

from settings import base_settings


class AuthUser(BaseModel):
    token: str | None = Field(default=None)

    def __init__(self, **data):
        if 'token' not in data or data['token'] is None:
            data['token'] = base_settings.test_user_token
        super().__init__(**data)


class Authentication(BaseModel):
    auth_token: str | None = None
    user: AuthUser | None = None

    def __init__(self, **data):
        if 'user' not in data or data['user'] is None:
            data['user'] = AuthUser()
        super().__init__(**data)

    @model_validator(mode='after')
    def validate_root(self) -> 'Authentication':
        if (not self.auth_token) and (not self.user.token):
            raise ValueError(
                'Please provide "auth_token"'
            )

        return self