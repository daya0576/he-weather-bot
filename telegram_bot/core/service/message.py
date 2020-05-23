# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

import pytz

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def send_weather_forecast(bot, chat_id: str):
    tz = pytz.timezone('Asia/Shanghai')
    cur_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    logger.info("Sending weather forecast...")
    bot.send_message(chat_id=chat_id, text=f"测试 - 定时任务触发的天气预报({cur_time})：")
    logger.info("Sending weather forecast image...")
    bot.send_photo(chat_id=chat_id, photo=f"http://wttr.in/上海浦东_0pq.png?2FnM&lang=zh-cn&{datetime.now(tz).timestamp()}")
    logger.info("Sent!")


def send_weather_forecast_to_channel(bot):
    chat_ids = os.environ["CHAT_IDS"].split(',')
    for chat_id in chat_ids:
        send_weather_forecast(bot, chat_id)
