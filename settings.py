from pydantic_settings import BaseSettings, SettingsConfigDict


class TestUser(BaseSettings):
    token: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    base_url: str
    test_user_token: str

    @property
    def api_url(self) -> str:
        return f'{self.base_url}/public/v2/'


base_settings = Settings()
