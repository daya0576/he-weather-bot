import re

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.settings import settings
from telegram_bot.telegram.bot import bot


async def handle_errors(*args, **partial_data):
    raise Exception(str(args))


if settings.DEV is not None:
    storage = MemoryStorage()
else:
    m = re.match(r"redis://:(.+)@(.+):(.+)", settings.REDIS_URL)
    password, host, port = m.group(1), m.group(2), m.group(3)
    storage = RedisStorage(host=host, port=port, password=password)

dp = Dispatcher(bot, storage=storage)
# dp.register_errors_handler(handle_errors)
dp.middleware.setup(LoggingMiddleware())
