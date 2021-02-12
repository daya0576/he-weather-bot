from aiogram import types
from aiogram.types import ContentType

from telegram_bot.service import message_service
from telegram_bot.telegram.dispatcher import dp


@dp.message_handler(commands=['weather'])
async def handle_weather(message: types.Message) -> None:
    await message_service.send_weather_text_to_chat(dp.bot, message.chat.id, location="shanghai")


@dp.message_handler(commands=['help'])
async def handle_help(message: types.Message) -> None:
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=ContentType.LOCATION)
@dp.message_handler(content_types=ContentType.VENUE)
async def handle_location(message: types.Message) -> None:
    if message.location:
        await message.reply(f"latitude: {message.location.latitude}, "
                            f"longitude: {message.location.longitude}")
    else:
        await message.reply("location is null!!")
