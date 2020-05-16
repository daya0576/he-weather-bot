# -*- coding: utf-8 -*-

import logging
import os

import telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def weather_forecast(request):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    default = "/start"
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id

        if update.message.text and update.message.text == '/start':
            bot.send_photo(chat_id=chat_id, photo="http://wttr.in/上海浦东_0pq.png?2FnM&lang=zh-cn")
            return
        else:
            bot.sendMessage(chat_id=chat_id, text=default)
