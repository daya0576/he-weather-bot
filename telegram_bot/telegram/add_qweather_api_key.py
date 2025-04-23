from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from loguru import logger

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_weather
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.telegram.dispatcher import dp


class Form(StatesGroup):
    key = State()


@dp.message_handler(commands="set_api_key")
async def update_api_key(message: types.Message):
    await Form.key.set()
    tutorial = "[教程](https://github.com/daya0576/he-weather-bot/wiki/%E5%92%8C%E9%A3%8E%E5%A4%A9%E6%B0%94-API-KEY-%E5%88%9B%E5%BB%BA%E6%95%99%E7%A8%8B)"
    await TelegramMessageService.send_markdown(
        dp.bot, message.chat.id, f"请回复和风天气 API KEY {tutorial}。 /cancel"
    )


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply("已取消")


@dp.message_handler(state=Form.key, content_types=ContentType.TEXT)
async def process_api_key(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    key = message.text.strip()

    try:
        assert "," in key
        host, key = key.split(",", 1)
    except Exception:
        await message.reply("请使用正确的格式: `<API Host>,<API Key>`。\n")
        return
    try:
        location = Location("", 39, 116, "utc", host=host, key=key)
        result = await he_weather.get_weather_forecast(location)
        assert result is not None
    except Exception as e:
        logger.exception(e)
        return await message.reply("API KEY 无效，请检查后重试。\n")

    with get_db_session() as db:
        key = crud.update_or_create_api_key(db, chat_id, host, key)
        await message.reply(f"已更新和风天气 API KEY: {str(key.key)}。\n")

    # Finish conversation
    await state.finish()
