from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.settings import dispatcher_storage
from telegram_bot.telegram.bot import bot

"""
help - 帮助
weather - 获取实时天气
change_location - 更新位置
sub - 订阅天气预报
unsub - 关闭订阅
update_sub_hour - 自定义推送时间
"""
dp = Dispatcher(bot, storage=dispatcher_storage)
dp.middleware.setup(LoggingMiddleware())
