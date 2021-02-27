from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str
    PROXY: str
    HE_WEATHER_API_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str = ""
    SENTRY_URL: str = ""
    ENV: str = "production"


settings = Settings()
