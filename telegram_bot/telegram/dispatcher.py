from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.settings import dispatcher_storage
from telegram_bot.telegram.bot import bot

"""
help - 帮助
weather - 获取实时天气
set_location - 更新位置
subscribe - 开启订阅
unsubscribe - 关闭订阅
set_ding_bot - 新增钉钉机器人同步
delete_ding_bot - 移除钉钉同步
"""
dp = Dispatcher(bot, storage=dispatcher_storage)
dp.middleware.setup(LoggingMiddleware())
