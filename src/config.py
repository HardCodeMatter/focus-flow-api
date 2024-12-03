from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int

    model_config = SettingsConfigDict(
        env_file='.env',
    )


settings: Settings = Settings()
