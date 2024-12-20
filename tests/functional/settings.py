from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    redis_host: str = Field("127.0.0.1")
    redis_port: int = Field(6379)

    postgres_db: str = Field("sott_real_estate_db")
    postgres_user: str = Field("postgres")
    postgres_password: str = Field("13db_sott_real_estate_db13")
    postgres_host: str = Field("127.0.0.1")
    postgres_port: int = Field(5433)

    service_host: str = Field("127.0.0.1")
    service_port: str | int = Field(5001)

    @property
    def postgres_credentials(self) -> dict:
        return {
            "dbname": self.postgres_db,
            "user": self.postgres_user,
            "password": self.postgres_password,
            "host": self.postgres_host,
            "port": self.postgres_port,
        }

    @property
    def service_url(self):
        return f"http://{self.service_host}:{self.service_port}"


test_settings = TestSettings()
