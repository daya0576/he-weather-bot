# -*- coding: utf-8 -*-

import os

import telegram
import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger
from telegram.ext import Dispatcher, CommandHandler

app = FastAPI()
bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cron")
def cron_handler():
    # send_weather_forecast_to_channel(bot)
    return 'ok'


@app.post('/hook')
def webhook_handler(request: Request):
    """Set route /hook with POST method will trigger this method."""
    update = telegram.Update.de_json(request.get(force=True), bot)

    # Update dispatcher process that handler to process this message
    dispatcher.process_update(update)

    return 'ok'


def reply_handler(bot, update):
    chat_id = update.message.chat.id
    from telegram_bot.biz.message import send_weather_forecast
    send_weather_forecast(bot, chat_id)
    logger.info("ok")


dispatcher = Dispatcher(bot, None)
# dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler("weather", reply_handler))

if __name__ == '__main__':
    uvicorn.run("telegram_bot:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
