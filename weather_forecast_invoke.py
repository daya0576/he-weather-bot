# -*- coding: utf-8 -*-

import os
from datetime import datetime

import pytz
import telegram


def weather_forecast(request):
    default = "/start"
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id

        if update.message.text and update.message.text == '/start':
            tz = pytz.timezone('Asia/Shanghai')
            bot.send_photo(chat_id=chat_id,
                           photo=f"http://wttr.in/上海浦东_0pq.png?2FnM&lang=zh-cn&{datetime.now(tz).timestamp()}")
            return
        else:
            bot.sendMessage(chat_id=chat_id, text=default)
