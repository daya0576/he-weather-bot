import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

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


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='state')
async def update_location(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.reply((str(current_state)))


@dp.message_handler(commands='change_location')
async def update_location(message: types.Message):
    await Form.location.set()
    await dp.bot.send_message(message.chat.id, "Hi！输入您所在的城市，或者发送定位")


@dp.message_handler(state=Form.location, content_types=ContentType.LOCATION)
@dp.message_handler(state=Form.location, content_types=ContentType.VENUE)
@dp.message_handler(state=Form.location, content_types=ContentType.TEXT)
async def process_location(message: types.Message, state: FSMContext):
    location = _get_location_from_message(message)
    if not location:
        return await message.reply("找不到输入的城市，试试其他关键字")

    user = crud.update_or_create_user(SessionLocal(), message.chat.id, location)
    await message.reply(f"城市信息已更新：{location.province}{user.city_name}({user.latitude},{user.longitude})\n"
                        f"{location.url}")

    # Finish conversation
    await state.finish()
