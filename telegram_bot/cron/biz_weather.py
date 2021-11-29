
from telegram_bot.database import models
from telegram_bot.intergration import he_weather
from telegram_bot.service.dingtalk import DingBotMessageService
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.settings import aio_lru_cache_1h, aio_lru_cache_48h
from telegram_bot.telegram.dispatcher import dp


@aio_lru_cache_1h
async def cron_send_weather(chat: models.Chat, ding_bot: models.DingBots):
    text = await he_weather.get_weather_forecast(chat.location)
    await TelegramMessageService.send_text(dp.bot, chat.chat_id, text)
    if ding_bot:
        await DingBotMessageService.send_text(ding_bot.token, text)

    # 注意：必须返回值，以确保缓存生效
    return True


@aio_lru_cache_48h
async def cron_send_warning(chat: models.Chat, ding_bot: models.DingBots):
    if warnModel := await he_weather.get_weather_warning(chat.location):
        await TelegramMessageService.send_text(dp.bot, chat.chat_id, str(warnModel))
        if ding_bot:
            await DingBotMessageService.send_text(ding_bot.token, str(warnModel))
        return True
