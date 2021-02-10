from aiogram import Bot

from telegram_bot.settings import settings

bot = Bot(
    token=settings.TELEGRAM_BOT_API_KEY.get_secret_value(),
    proxy=settings.PROXY
)
# bot.timeout = 3
