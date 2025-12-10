from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    SQLITE_URL: str
    POSTGRES_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str

    @property
    def DATABASE_URL(self) -> str:
        return self.SQLITE_URL if self.DEBUG else self.POSTGRES_URL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
