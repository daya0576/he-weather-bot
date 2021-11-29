from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.settings import dispatcher_storage
from telegram_bot.telegram.bot import bot

"""
help - 帮助
weather - 获取实时天气
update_location - 更新位置
subscribe - 开启订阅
unsubscribe - 关闭订阅
ding_token - 钉钉同步
"""
dp = Dispatcher(bot, storage=dispatcher_storage)
dp.middleware.setup(LoggingMiddleware())
