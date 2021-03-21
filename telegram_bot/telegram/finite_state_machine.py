from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_location_client
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.service.message import TelegramMessageService
from telegram_bot.telegram.components.keyboard_markup_factory import KeyboardMarkUpFactory, WELCOME_TEXT
from telegram_bot.telegram.dispatcher import dp


async def _get_location_from_message(message: types.Message) -> "Location":
    if message.location:
        return await he_location_client.get_location_by_lat_lon(
            message.location.latitude,
            message.location.longitude
        )

    return await he_location_client.get_location_by_city_keywords(
        message.text.strip()
    )


class Form(StatesGroup):
    # language = State()
    location = State()


@dp.message_handler(commands='change_location')
async def update_location(message: types.Message):
    await Form.location.set()
    await TelegramMessageService.send_text(dp.bot, message.chat.id, "Hi！发送当前定位，或者输入城市关键字")


@dp.message_handler(state=Form.location, content_types=ContentType.LOCATION)
@dp.message_handler(state=Form.location, content_types=ContentType.VENUE)
@dp.message_handler(state=Form.location, content_types=ContentType.TEXT)
async def process_location(message: types.Message, state: FSMContext):
    location = await _get_location_from_message(message)
    if not location:
        return await message.reply("找不到输入的城市，试试其他关键字")

    # 更新用户所属位置
    with get_db_session() as db:
        user = crud.update_or_create_user(db, message.chat.id, location)
    await message.reply(f"城市信息已更新：{location.province}{user.city_name}"
                        f"({user.latitude},{user.longitude})\n{location.url}")

    reply_markup = KeyboardMarkUpFactory.build_main_menu(user)
    await TelegramMessageService.send_keyboard_markup(dp.bot, message.chat.id, WELCOME_TEXT, reply_markup)

    # Finish conversation
    await state.finish()
