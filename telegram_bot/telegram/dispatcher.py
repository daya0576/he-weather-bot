from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.telegram.bot import bot


async def handle_errors(*args, **partial_data):
    raise Exception(str(args))


# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# dp.register_errors_handler(handle_errors)
dp.middleware.setup(LoggingMiddleware())
