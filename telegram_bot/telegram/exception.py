from aiogram import types
from aiogram.utils.exceptions import BotBlocked, MessageNotModified
from loguru import logger
from sentry_sdk import capture_exception

from telegram_bot.telegram.dispatcher import dp


@dp.errors_handler(exception=BotBlocked)
async def global_error_handler(update: types.Update, e):
    logger.warning(e)
    return True


@dp.errors_handler(exception=MessageNotModified)
async def global_error_handler(update: types.Update, e):
    logger.warning(e)
    return True


@dp.errors_handler(exception=Exception)
async def global_error_handler(update: types.Update, e: Exception):
    capture_exception(e)
    logger.exception(e)
    return True
