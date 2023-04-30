import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_weather
from telegram_bot.service.dingtalk import DingBotMessageService
from telegram_bot.service.telegram import TelegramMessageService
from telegram_bot.telegram.callbacks import registered
from telegram_bot.telegram.dispatcher import dp

RE_PATTERN = re.compile(
    r"https://oapi\.dingtalk\.com/robot/send\?access_token=([a-zA-Z0-9]+)"
)


async def extra_ding_token_from_message(text) -> str:
    if not text:
        return ""
    if m := RE_PATTERN.match(text.strip()):
        return m.group(1)


class Form(StatesGroup):
    set_ding_token = State()
    set_location_alias = State()


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


@dp.message_handler(commands="set_ding_bot")
@registered
async def update_ding_token(message: types.Message):
    await Form.set_location_alias.set()
    await TelegramMessageService.send_text(dp.bot, message.chat.id, "Hi！请回复定位别名，例如上海外滩")


@dp.message_handler(commands="delete_ding_bot")
@registered
async def remove_ding_token(message: types.Message):
    with get_db_session() as db:
        is_delete_bot = crud.remove_ding_bot(db, message.chat.id)

    if is_delete_bot:
        return await message.reply("已取消关联")
    else:
        return await message.reply("不存在关联")


@dp.message_handler(state=Form.set_ding_token, content_types=ContentType.TEXT)
@dp.message_handler(state=Form.set_ding_token, content_types=ContentType.ANY)
async def process_ding_token(message: types.Message, state: FSMContext):
    ding_bot_token = await extra_ding_token_from_message(message.text)
    if not ding_bot_token:
        return await message.reply(
            "机器人的Webhook地址非法!"
            "\n参考格式：https://oapi.dingtalk.com/robot/send?access_token=XXXXXX"
            "\n取消输入：/cancel"
        )

    with get_db_session() as db:
        crud.update_or_create_ding_bot(db, message.chat.id, ding_bot_token)

    # 发送测试消息
    with get_db_session() as db:
        chat = crud.get_user(db, chat_id=message.chat.id)
    text = await he_weather.get_weather_forecast(chat.location)
    await DingBotMessageService.send_text(ding_bot_token, text)
    await message.reply("钉钉Token关联成功，请注意查收测试消息~")
    await state.finish()


@dp.message_handler(state=Form.set_location_alias, content_types=ContentType.TEXT)
@dp.message_handler(state=Form.set_location_alias, content_types=ContentType.ANY)
async def process_ding_token_alias(message: types.Message, state: FSMContext):
    location_name = message.text.strip()
    if not location_name or len(location_name) > 10:
        return await message.reply("别名长度过长！")

    with get_db_session() as db:
        crud.update_location_name(db, message.chat.id, location_name)

    await TelegramMessageService.send_text(
        dp.bot, message.chat.id, "请输入自定义机器人Webhook地址"
    )
    await Form.set_ding_token.set()
