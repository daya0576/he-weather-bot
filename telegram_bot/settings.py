from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urlparse

from aiocache import cached, Cache
from aiogram.contrib.fsm_storage.redis import RedisStorage
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str
    HE_WEATHER_API_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: Optional[str] = ""
    SENTRY_URL: Optional[str] = ""
    ENV: str = "production"
    CACHE_TTL: int = 60 * 59
    DEFAULT_TIMEZONE: str = "Asia/Shanghai"
    PROXY: Optional[str] = ""
    DO_RELEASE: bool = False
    DOMAIN: Optional[str] = "localhost"

    @property
    def is_production(self):
        return self.ENV == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@dataclass
class RedisConfig:
    host: str
    port: int
    user: Optional[str]
    password: Optional[str]

    def __init__(self, url) -> None:
        parsed_redis_url = urlparse(url)
        if parsed_redis_url.hostname is None or parsed_redis_url.port is None:
            raise ValueError(f"invalid redis url: {url}")
        self.user, self.password, self.host, self.port = (
            parsed_redis_url.username,
            parsed_redis_url.password,
            parsed_redis_url.hostname,
            int(parsed_redis_url.port),
        )


settings = Settings()
redis_config = RedisConfig(settings.REDIS_URL)
dispatcher_storage = RedisStorage(
    host=redis_config.host, port=redis_config.port, password=redis_config.password
)
aio_lru_cache_partial = partial(
    cached,
    cache=Cache.REDIS,
    endpoint=redis_config.host,
    port=redis_config.port,
    password=redis_config.password,
)
aio_lru_cache_1h = aio_lru_cache_partial(ttl=settings.CACHE_TTL)
aio_lru_cache_24h = aio_lru_cache_partial(ttl=settings.CACHE_TTL * 24)
