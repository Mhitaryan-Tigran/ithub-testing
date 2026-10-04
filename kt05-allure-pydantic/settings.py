from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="PETSTORE_")

    base_url: str = "https://petstore.swagger.io/v2"
    timeout: float = 15.0
    api_key: str = "special-key"


settings = Settings()
