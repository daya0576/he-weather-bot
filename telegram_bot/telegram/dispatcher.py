from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.telegram.bot import bot


async def handle_errors():
    raise Exception


dp = Dispatcher(bot)
dp.register_errors_handler(handle_errors)
dp.middleware.setup(LoggingMiddleware())
