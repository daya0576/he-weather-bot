from aiogram import types
from aiogram.types import ContentType

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.intergration import he_weather
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.finite_state_machine import update_location

WELCOME_TEXT = """
基于「和风」的天气预报机器人。根据用户位置查询实时天气，并每天自动播报。

如有任何问题，请联系 @daya0576    
"""


@dp.message_handler(commands=['weather'])
async def handle_weather(message: types.Message) -> None:
    chat_id = message.chat.id
    user = crud.get_user(SessionLocal(), chat_id)
    if not user:
        return await update_location(message)

    text = he_weather.get_weather_forecast(user.location)
    await dp.bot.send_message(chat_id=chat_id, text=text)


@dp.message_handler(commands=['help', 'start'])
@dp.message_handler(content_types=ContentType.ANY)
async def handle_help(message: types.Message) -> None:
    keyboard_markup = types.InlineKeyboardMarkup(row_width=6)

    keyboard_markup.add(
        types.InlineKeyboardButton('获取实时天气', callback_data='weather'),
    )

    inline_buttons = (
        types.InlineKeyboardButton('更新位置', callback_data="edit"),
        # types.InlineKeyboardButton('更新位置', callback_data="edit"),
        types.InlineKeyboardButton('关注项目✨', url="https://github.com/daya0576/he_weather_bot"),
        # ('开启订阅', 'enable'),
        # ('关闭订阅', 'disable'),
    )
    keyboard_markup.row(*inline_buttons)

    await dp.bot.send_message(message.chat.id, WELCOME_TEXT, parse_mode='Markdown', reply_markup=keyboard_markup)


@dp.callback_query_handler(text='weather')
@dp.callback_query_handler(text='edit')
@dp.callback_query_handler(text='enable')
@dp.callback_query_handler(text='disable')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    if answer_data == 'weather':
        await handle_weather(query.message)
    elif answer_data == 'edit':
        await update_location(query.message)

    await query.answer('')
