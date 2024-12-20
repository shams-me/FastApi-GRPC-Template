from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    project_name: str = "auth-service"
    GRPC_PORT: int = Field(5101, alias="grpc_port")
    REST_PORT: int = Field(5102, alias="rest_port")

    postgres_db: str = Field("postgres_db", alias="POSTGRES_DB")
    postgres_user: str = Field("postgres_user", alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_engine_echo: bool = False

    user_service_host: str = Field("localhost", alias="USER_SERVICE_HOST")
    user_service_port: int = Field(5001, alias="USER_SERVICE_PORT")

    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")

    access_expires: int = 15  # 15 min
    refresh_expires: int = 60 * 24 * 10  # 10 days
    auth_jwt_secret_key: str = Field("auth_jwt_secret_key", alias="AUTH_JWT_SECRET_KEY")

    # YANDEX OAUTH SETTINGS
    YANDEX_CLIENT_ID: str = Field("5fae3168fba440d48acd176ccd9f4a85", alias="YANDEX_CLIENT_ID")
    YANDEX_CLIENT_SECRET: str = Field("95f335c9847e4f93af00d7980a1b7c30", alias="YANDEX_CLIENT_SECRET")
    YANDEX_REDIRECT_URI: str = Field(
        "http://localhost/auth/api/auth/login/yandex/redirect",
        alias="YANDEX_REDIRECT_URI",
    )

    @property
    def pg_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        extra = "allow"


settings: Settings = Settings()
