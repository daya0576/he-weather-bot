import functools

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from loguru import logger

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session


def service_template(f):
    @functools.wraps(f)
    async def inner(bot: Bot, chat_id: str, *args, **kwargs):
        try:
            await f(bot, chat_id, *args, **kwargs)
        except (BotBlocked, UserDeactivated, BotBlocked) as e:
            logger.warning(f"bot blocked by {chat_id},{str(e)}")
            with get_db_session() as db:
                crud.update_user_status(db, chat_id, False)
        else:
            logger.info(f"message send to {chat_id},args={args},kwargs={kwargs}")

    return inner


class TelegramMessageService:
    @staticmethod
    @service_template
    async def send_text(bot: Bot, chat_id: str, text: str):
        await bot.send_message(chat_id=chat_id, text=text)

    @staticmethod
    @service_template
    async def send_markdown(bot: Bot, chat_id: str, text: str):
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='MarkdownV2')

    @staticmethod
    @service_template
    async def send_keyboard_markup(bot: Bot, chat_id: str, text: str, reply_markup=None, parse_mode="MarkdownV2"):
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)
