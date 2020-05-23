# -*- coding: utf-8 -*-

import logging
import os

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters

from telegram_bot.core.service.message import send_weather_forecast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))


@app.route('/', methods=['get'])
def index():
    return 'ok'


@app.route('/cron', methods=['POST'])
def cron_handler():
    chat_ids = os.environ["CHAT_IDS"].split(',')
    for chat_id in chat_ids:
        send_weather_forecast(bot, chat_id)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)

    return 'ok'


def reply_handler(bot, update):
    # weather forecast
    logger.info("Sending weather forecast...")
    chat_id = update.message.chat.id
    logger.info("Sending weather forecast image...")
    send_weather_forecast(bot, chat_id)
    logger.info("Sent!")


dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
