from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_REFRESH_TOKEN_EXPIRE_DAYS: int

    DATABASE_URL: str
    DATABASE_ECHO: bool

    model_config = SettingsConfigDict(
        env_file='.env',
    )


settings: Settings = Settings()
