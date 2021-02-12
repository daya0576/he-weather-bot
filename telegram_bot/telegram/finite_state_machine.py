from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.intergration import he_location_client
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.telegram.dispatcher import dp


def _get_location_from_message(message: types.Message) -> "Location":
    if message.location:
        return he_location_client.get_location_by_lat_lon(
            message.location.latitude,
            message.location.longitude
        )

    return he_location_client.get_location_by_city_keywords(
        message.text.strip()
    )


class Form(StatesGroup):
    # language = State()
    location = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.location.set()

    await message.reply("Hi！输入您所在的城市，或者发送定位")


@dp.message_handler(state=Form.location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location = _get_location_from_message(message)
        if not location:
            return await message.reply("找不到输入的城市，试试其他关键字")

        crud.update_or_create_user(SessionLocal(), message.chat.id, location)
        await message.reply(f"城市信息：{location}")

    # Finish conversation
    await state.finish()
