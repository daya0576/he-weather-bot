from aiogram import Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.service import message_service
from telegram_bot.telegram.bot import bot


def handle_errors():
    raise Exception


async def send_weather(message: types.Message) -> None:
    await message_service.send_weather_text_to_chat(dispatcher.bot, message.chat.id)


async def send_weather_photo(message: types.Message) -> None:
    await message_service.send_weather_photo_to_chat(dispatcher.bot, message.chat.id)


async def echo_health_check(message: types.Message) -> None:
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


dispatcher = Dispatcher(bot)
dispatcher.middleware.setup(LoggingMiddleware())
# dispatcher.register_errors_handler(handle_errors)
dispatcher.register_message_handler(echo_health_check, commands=['help'])
dispatcher.register_message_handler(send_weather_photo, commands=['weather'])
