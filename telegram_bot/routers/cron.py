import asyncio

from aiogram.utils.exceptions import BotBlocked
from fastapi import APIRouter
from fastapi.logger import logger

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.database.models import User
from telegram_bot.intergration import he_weather
from telegram_bot.telegram.dispatcher import dp

router = APIRouter()


@router.get("/")
async def index():
    logger.info("test...")
    return {"message": "Hello World"}


@router.get("/users")
async def users():
    return crud.get_users(SessionLocal())


@router.get("/cron")
async def cron_handler():
    users = crud.get_users(SessionLocal())

    # 待单独抽出为 service
    async def _inner(user: User):
        text = he_weather.get_weather_forecast(user.location)
        try:
            await dp.bot.send_message(chat_id=user.chat_id, text=text)
        except BotBlocked:
            logger.warn(f"bot blocked by {user}")

    # 并行处理，单个 exception 不中断其他任务
    results = await asyncio.gather(
        *[_inner(user) for user in users],
        return_exceptions=True
    )
    # 汇总异常处理
    for result in results:
        if isinstance(result, Exception):
            raise Exception(result)

    return 'ok'
