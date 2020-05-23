# -*- coding: utf-8 -*-
import logging
import os

from telegram_bot.core.service.heweather import Weather

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def send_weather_forecast(bot, chat_id: str):
    logger.info("Sending weather forecast...")
    bot.send_message(chat_id=chat_id, text=Weather().get_weather())
    # logger.info("Sending weather forecast image...")
    # bot.send_photo(chat_id=chat_id, photo=f"http://wttr.in/上海浦东_0pq.png?2FnM&lang=zh-cn&{datetime.now(tz).timestamp()}")
    logger.info("Sent!")


def send_weather_forecast_to_channel(bot):
    chat_ids = os.environ["CHAT_IDS"].split(',')
    for chat_id in chat_ids:
        send_weather_forecast(bot, chat_id)
