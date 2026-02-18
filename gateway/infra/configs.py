from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    redis_password: str
    redis_host: str

    @property
    def conn_url(self):
        return f"redis://:{self.redis_password}@{self.redis_host}:6379"
