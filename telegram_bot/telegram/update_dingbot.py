import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.service.message import TelegramMessageService
from telegram_bot.telegram.callbacks import registered
from telegram_bot.telegram.dispatcher import dp

RE_PATTERN = re.compile(r'https://oapi\.dingtalk\.com/robot/send\?access_token=([a-zA-Z0-9]+)')


async def extra_ding_token_from_message(text) -> str:
    if not text:
        return ""
    if m := RE_PATTERN.match(text.strip()):
        return m.group(1)


class Form(StatesGroup):
    ding_token = State()


@dp.message_handler(commands='ding_token')
@registered
async def update_ding_token(message: types.Message):
    await Form.ding_token.set()
    await TelegramMessageService.send_text(dp.bot, message.chat.id, "Hi！请输入机器人的Webhook地址")


@dp.message_handler(state=Form.ding_token, content_types=ContentType.TEXT)
async def process_ding_token(message: types.Message, state: FSMContext):
    ding_token = await extra_ding_token_from_message(message.text)
    if not ding_token:
        await message.reply("机器人的Webhook地址非法，参考：https://oapi.dingtalk.com/robot/send?access_token=XXXXXX:")
        await state.finish()
        return

    with get_db_session() as db:
        crud.update_or_create_ding_bot(db, message.chat.id, ding_token)
    await message.reply("钉钉Token已关联！")
    await state.finish()