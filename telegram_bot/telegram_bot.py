# -*- coding: utf-8 -*-

import os

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters

from telegram_bot.core.service.message import send_weather_forecast, send_weather_forecast_to_channel

app = Flask(__name__)
bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))


@app.route('/', methods=['get'])
def index():
    return 'OK'


@app.route('/cron', methods=['GET'])
def cron_handler():
    send_weather_forecast_to_channel(bot)
    return 'ok'


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)

    return 'ok'


def reply_handler(bot, update):
    chat_id = update.message.chat.id
    send_weather_forecast(bot, chat_id)


dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
