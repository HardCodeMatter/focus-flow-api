from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int

    DATABASE_URL: str
    DATABASE_ECHO: bool
    DATABASE_POOL_SIZE: int

    model_config = SettingsConfigDict(
        env_file='.env',
    )


settings: Settings = Settings()
