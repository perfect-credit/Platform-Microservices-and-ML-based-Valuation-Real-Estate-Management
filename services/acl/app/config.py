from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    PORT: int
    DB_URI: str

    # JWT configuration
    JWT_KEY: str
    JWT_EXPIRE: int
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        extra="forbid",
    )


def get_settings() -> AppConfig:
    return AppConfig()


settings: AppConfig = get_settings()
