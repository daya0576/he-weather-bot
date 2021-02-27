import functools

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked
from loguru import logger


def service_template(f):
    @functools.wraps(f)
    async def inner(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except BotBlocked:
            logger.warning(f"bot blocked by {args}")

    return inner


class TelegramMessageService:
    @staticmethod
    @service_template
    async def send_text(bot: Bot, chat_id, text):
        await bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    @service_template
    async def send_keyboard_markup(bot: Bot, chat_id, text, keyboard_markup):
        await bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=keyboard_markup)
