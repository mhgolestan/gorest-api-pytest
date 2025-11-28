import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestUser(BaseSettings):
    token: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env' if os.path.exists('.env') else None,
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    base_url: str = Field(default=os.getenv('BASE_URL', ''))
    test_user_token: str = Field(default=os.getenv('TEST_USER_TOKEN', ''))

    @property
    def api_url(self) -> str:
        return f'{self.base_url}/public/v2/'


base_settings = Settings()
