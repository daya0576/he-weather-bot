from loguru import logger

from telegram_bot.database import models
from telegram_bot.intergration import he_weather
from telegram_bot.settings import aio_lru_cache_1h, aio_lru_cache_48h
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.service.message import TelegramMessageService


@aio_lru_cache_1h
async def biz_send_weather(chat: models.Chat, user_cur_hour: str):
    text = await he_weather.get_weather_forecast(chat.location)
    await TelegramMessageService.send_text(dp.bot, chat.chat_id, text)
    logger.info(f"[cron]send_weather_to_user,{user_cur_hour},{chat}")
    return True


@aio_lru_cache_48h
async def biz_send_warning(chat: models.Chat):
    if warnModel := await he_weather.get_weather_warning(chat.location):
        await TelegramMessageService.send_text(dp.bot, chat.chat_id, str(warnModel))
        logger.info(f"[cron]send_warning_to_user,success,{chat}")
        return True
