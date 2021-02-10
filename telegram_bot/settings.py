from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TELEGRAM_BOT_API_KEY: SecretStr
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str
    PROXY: str


settings = Settings()
