import re
from dataclasses import dataclass
from functools import partial

from aiocache import cached, Cache
from aiogram.contrib.fsm_storage.redis import RedisStorage
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str
    DOMAIN: str
    PROXY: str
    HE_WEATHER_API_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str = ""
    SENTRY_URL: str = ""
    ENV: str = "production"
    CACHE_TTL: int = 60 * 59
    DEFAULT_TIMEZONE: str = "Asia/Shanghai"
    DO_RELEASE: bool = False

    @property
    def is_production(self):
        return self.ENV == "production"


@dataclass
class RedisConfig:
    host: str
    port: str
    password: str

    def __init__(self, url) -> None:
        m = re.match(r"redis://:(.*)@(.*):(.*)", url)
        self.password, self.host, self.port = m.group(1), m.group(2), m.group(3)


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
