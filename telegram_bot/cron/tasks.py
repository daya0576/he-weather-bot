from typing import List
from telegram_bot.database import models
from telegram_bot.intergration import he_weather
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.service.dingtalk import DingBotMessageService
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.settings import aio_lru_cache_1h, aio_lru_cache_24h
from telegram_bot.telegram.dispatcher import dp


async def _do_send_weather_message(
    chat: models.Chat, ding_bot: models.DingBots, text: str
):
    await TelegramMessageService.send_text(dp.bot, chat.chat_id, text)
    if ding_bot:
        await DingBotMessageService.send_text(ding_bot.token, text)
    # 注意：必须返回值，以确保缓存生效
    return True


notify_with_1h_cache = aio_lru_cache_1h(_do_send_weather_message)
notify_with_24h_cache = aio_lru_cache_24h(_do_send_weather_message)


async def cron_send_weather(
    chat: models.Chat, locations: List[Location], ding_bot: models.DingBots
):
    """定时发送天气预报"""
    for location in locations:
        text = await he_weather.get_weather_forecast(location)
        await notify_with_1h_cache(chat, ding_bot, text)
    return True


async def cron_send_warning(chat: models.Chat, ding_bot: models.DingBots):
    """定时发送天气预警信息"""
    if warnModel := await he_weather.get_weather_warning(chat.location):
        # 预警信息可能持续超过 1h，故新增幂等操作
        # 如果 24h 内有新增预警信息，不影响发送
        await notify_with_24h_cache(chat, ding_bot, str(warnModel))
    return True
