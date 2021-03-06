from aiogram import types

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.intergration import he_weather
from telegram_bot.service.message import TelegramMessageService
from telegram_bot.telegram.components.keyboard_markup_factory import KeyboardMarkUp
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

    text = await he_weather.get_weather_forecast(user.location)
    await TelegramMessageService.send_text(dp.bot, chat_id, text)


@dp.message_handler(commands=['help', 'start'])
async def handle_help(message: types.Message) -> None:
    user = crud.get_user(SessionLocal(), message.chat.id)
    keyboard_markup = KeyboardMarkUp.get(user)
    await TelegramMessageService.send_keyboard_markup(dp.bot, message.chat.id, WELCOME_TEXT, keyboard_markup)


@dp.callback_query_handler(text='weather')
@dp.callback_query_handler(text='edit')
@dp.callback_query_handler(text='enable')
@dp.callback_query_handler(text='disable')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    if answer_data == 'weather':
        await handle_weather(query.message)
        await query.answer('')
    elif answer_data == 'edit':
        await update_location(query.message)
        await query.answer('')
    elif answer_data == 'enable' or answer_data == "disable":
        crud.update_user_status(SessionLocal(), query.message.chat.id, answer_data == 'enable')
        text = "已开启订阅" if answer_data == 'enable' else "已关闭订阅"
        user = crud.get_user(SessionLocal(), query.message.chat.id)
        await query.answer(text)
        await query.message.edit_reply_markup(KeyboardMarkUp.get(user))

    await query.answer("")
