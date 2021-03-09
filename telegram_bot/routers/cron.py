import asyncio

from fastapi import APIRouter, Depends
from sentry_sdk import capture_exception
from sqlalchemy.orm import Session

from telegram_bot.database import crud
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.database.models import Chat
from telegram_bot.intergration import he_weather
from telegram_bot.service.message import TelegramMessageService
from telegram_bot.telegram.dispatcher import dp

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/users")
async def users():
    with get_db_session() as db:
        return crud.get_users(db)


@router.get("/cron")
async def cron_handler(db: Session = Depends(get_db)):
    all_users = (user for user in crud.get_users(db) if user.is_active)

    async def _inner(user: Chat):
        text = he_weather.get_weather_forecast(user.location)
        await TelegramMessageService.send_text(dp.bot, user.chat_id, text)

    # 并行处理，单个任务 exception 不中断其他任务
    results = await asyncio.gather(
        *(_inner(user) for user in all_users),
        return_exceptions=True
    )

    # 汇总异常处理
    for result in results:
        if isinstance(result, Exception):
            capture_exception(result)

    return {"count": len(results)}
