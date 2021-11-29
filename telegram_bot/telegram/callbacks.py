from aiogram import types

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_weather
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.keyboard.keyboard_markup_factory import KeyboardMarkUpFactory, WELCOME_TEXT, GET_WEATHER, \
    UPDATE_LOCATION, ENABLE_SUB, DISABLE_SUB, UPDATE_SUB_CRON, BACK, HOURS
from telegram_bot.telegram.update_location import update_location


def registered(func):
    async def wrapper(message: types.Message):
        chat_id = message.chat.id
        with get_db_session() as db:
            user = crud.get_user(db, chat_id)

        if not user:
            return await update_location(message)

        await func(message)

    return wrapper


@dp.message_handler(commands=['weather'])
@registered
async def handle_weather(message: types.Message) -> None:
    chat_id = message.chat.id
    with get_db_session() as db:
        user = crud.get_user(db, chat_id)

    text = await he_weather.get_weather_forecast(user.location)
    await TelegramMessageService.send_text(dp.bot, chat_id, text)


@dp.message_handler(commands=['id'])
@registered
async def handle_chat_id(message: types.Message) -> None:
    chat_id = message.chat.id
    await TelegramMessageService.send_text(dp.bot, chat_id, chat_id)


@dp.message_handler(commands=['help', 'start'])
async def handle_help(message: types.Message) -> None:
    with get_db_session() as db:
        user = crud.get_user(db, message.chat.id)
    reply_markup = KeyboardMarkUpFactory.build_main_menu(user)
    await TelegramMessageService.send_keyboard_markup(dp.bot, message.chat.id, WELCOME_TEXT, reply_markup)


@dp.message_handler(commands=['subscribe'])
@registered
async def handle_sub(message: types.Message) -> None:
    with get_db_session() as db:
        crud.update_user_status(db, message.chat.id, True)
        await TelegramMessageService.send_text(dp.bot, message.chat.id, "已开启定时订阅")

        user = crud.get_user(db, message.chat.id)
        reply_markup = KeyboardMarkUpFactory.build_cron_options(user)
        await TelegramMessageService.send_keyboard_markup(dp.bot, message.chat.id, WELCOME_TEXT, reply_markup)


@dp.message_handler(commands=['unsubscribe'])
@registered
async def handle_unsub(message: types.Message) -> None:
    with get_db_session() as db:
        crud.update_user_status(db, message.chat.id, False)
    await TelegramMessageService.send_text(dp.bot, message.chat.id, "已关闭定时订阅")


@dp.callback_query_handler(text=GET_WEATHER)
async def weather_callback_handler(query: types.CallbackQuery):
    await handle_weather(query.message)
    await query.answer('')


@dp.callback_query_handler(text=UPDATE_LOCATION)
async def location_callback_handler(query: types.CallbackQuery):
    await update_location(query.message)
    await query.answer('')


@dp.callback_query_handler(text=ENABLE_SUB)
@dp.callback_query_handler(text=DISABLE_SUB)
async def update_subscription_callback_handler(query: types.CallbackQuery):
    is_enable = query.data == ENABLE_SUB
    with get_db_session() as db:
        crud.update_user_status(db, query.message.chat.id, is_enable)
        text = "已开启订阅" if is_enable else "已关闭订阅"
        user = crud.get_user(db, query.message.chat.id)
        await query.answer(text)
        await query.message.edit_reply_markup(KeyboardMarkUpFactory.build_cron_options(user))


@dp.callback_query_handler(text=UPDATE_SUB_CRON)
async def sub_cron_callback_handler(query: types.CallbackQuery):
    with get_db_session() as db:
        user = crud.get_user(db, query.message.chat.id)
        await query.message.edit_reply_markup(
            KeyboardMarkUpFactory.build_cron_options(user)
        )
        await query.answer('')


@dp.callback_query_handler(text=BACK)
async def exit_callback_handler(query: types.CallbackQuery):
    with get_db_session() as db:
        user = crud.get_user(db, query.message.chat.id)
        await query.message.edit_reply_markup(
            KeyboardMarkUpFactory.build_main_menu(user)
        )
        await query.answer('')


@dp.callback_query_handler(lambda callback_query: callback_query.data in HOURS)
async def sub_cron_update_callback_handler(query: types.CallbackQuery):
    hour = query.data
    chat_id = query.message.chat.id

    with get_db_session() as db:
        # 激活用户
        crud.update_user_status(db, query.message.chat.id, True)
        user = crud.get_user(db, query.message.chat.id)

        # 新增/删除订阅
        cron_job, created = crud.create_or_delete_cron_job(db, chat_id, hour)
        if created:
            await query.answer("订阅成功")
        else:
            await query.answer("已取消")

        db.refresh(user)
        cron_sub_menu = KeyboardMarkUpFactory.build_cron_options(user)
        await query.message.edit_reply_markup(cron_sub_menu)
