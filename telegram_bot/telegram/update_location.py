from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_location_client, he_weather
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.telegram.dispatcher import dp


async def _get_location_from_message(message: types.Message) -> Optional["Location"]:
    # 1. 用户定位位置
    if message.location:
        return await he_location_client.get_location_by_lat_lon(
            message.location.latitude, message.location.longitude
        )

    # 2. 关键字定位
    return await he_location_client.get_location_by_city_keywords(message.text.strip())


class Form(StatesGroup):
    location = State()


@dp.message_handler(commands="set_location")
async def update_location(message: types.Message):
    await Form.location.set()
    await TelegramMessageService.send_text(
        dp.bot, message.chat.id, "请回复当前城市关键字，或者模糊定位。  /cancel"
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


@dp.message_handler(state=Form.location, content_types=ContentType.LOCATION)
@dp.message_handler(state=Form.location, content_types=ContentType.VENUE)
@dp.message_handler(state=Form.location, content_types=ContentType.TEXT)
async def process_location(message: types.Message, state: FSMContext):
    location = await _get_location_from_message(message)
    if not location:
        return await message.reply("找不到输入的城市，试试其他关键字 /cancel")

    # 更新用户所属位置
    with get_db_session() as db:
        user = crud.update_or_create_user_by_location(db, message.chat.id, location)
    await message.reply(
        f"城市信息已更新：{location.province}{user.city_name}"
        f"({user.latitude},{user.longitude})\n{location.url}"
    )

    # 更新位置后，发送天气预报
    text = await he_weather.get_weather_forecast(user.location)
    text = f"\n{text}"
    await TelegramMessageService.send_text(dp.bot, message.chat.id, text)

    # Finish conversation
    await state.finish()
