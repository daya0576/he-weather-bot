import asyncio

from fastapi import APIRouter
from loguru import logger

from telegram_bot.database import crud
from telegram_bot.database.database import SessionLocal
from telegram_bot.database.models import User
from telegram_bot.intergration import he_weather
from telegram_bot.service.message import TelegramMessageService
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
    all_users = crud.get_users(SessionLocal())

    async def _inner(user: User):
        text = await he_weather.get_weather_forecast(user.location)
        await TelegramMessageService.send_text(dp.bot, user.chat_id, text)

    # 并行处理，单个 exception 不中断其他任务
    results = await asyncio.gather(
        *[_inner(user) for user in all_users],
        return_exceptions=True
    )
    # 汇总异常处理
    for result in results:
        if isinstance(result, Exception):
            raise Exception(result)

    return 'ok'
