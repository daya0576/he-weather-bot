import asyncio

from fastapi import APIRouter, Depends
from sentry_sdk import capture_exception
from sqlalchemy.orm import Session

from telegram_bot.database import crud, models
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.intergration import he_weather
from telegram_bot.settings import aio_lru_cache
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.service.message import TelegramMessageService
from telegram_bot.util.date_util import DateUtil

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/users")
async def users():
    with get_db_session() as db:
        return crud.get_users(db)


@router.get("/cron_jobs")
async def users():
    with get_db_session() as db:
        return crud.get_active_cron_jobs_by_hour(db, )


@aio_lru_cache
async def send_weather_by(user: "models.Chat"):
    text = await he_weather.get_weather_forecast(user.location)
    await TelegramMessageService.send_text(dp.bot, user.chat_id, text)
    return True


@router.get("/cron")
async def cron_handler(db: Session = Depends(get_db)):
    # 筛选符合条件的用户会话
    all_active_users = [
        user for user in crud.get_users(db)
        if user.is_active and DateUtil.get_cur_hour(user.time_zone) in user.sub_hours
    ]

    # 并行处理 - 单个任务 exception 不中断其他任务
    results = await asyncio.gather(
        *(send_weather_by(user) for user in all_active_users),
        return_exceptions=True
    )

    # 汇总异常处理
    failed = success = 0
    for result in results:
        if isinstance(result, Exception):
            failed += 1
            capture_exception(result)
        elif result:
            success += 1

    return {"total": len(results), "failed": failed}
