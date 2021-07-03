from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from telegram_bot.database import crud
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.database.models import Chat
from telegram_bot.intergration import he_weather
from telegram_bot.scheduler import scheduler
from telegram_bot.scheduler.job import CronJobsExecutor
from telegram_bot.settings import aio_lru_cache_1h
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.service.message import TelegramMessageService
from telegram_bot.util.date_util import DateUtil

QPM_LIMIT = 500
ONE_MINUTE = 60 * 1000

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/users")
async def users():
    with get_db_session() as db:
        return crud.get_users(db)


@aio_lru_cache_1h
async def cron_send_weather_to_user(chat: Chat, user_cur_hour: str):
    text = await he_weather.get_weather_forecast(chat.location)
    await TelegramMessageService.send_text(dp.bot, chat.chat_id, text)
    logger.info(f"[cron]send_weather_to_user,{user_cur_hour},{chat}")
    return True


@router.get("/cron_send_weather_to_user")
async def weather_by_user(user_id: str, user_cur_hour: str):
    with get_db_session() as db:
        chat = crud.get_user(db, user_id)
    if not chat or not chat.is_active:
        return {"message": "USER_NOT_FOUND"}

    await cron_send_weather_to_user(chat, user_cur_hour)


@router.get("/cron")
async def cron_handler(db: Session = Depends(get_db)):
    # 限流: https://dev.qweather.com/docs/start/glossary#qpm
    mil_seconds_interval = (ONE_MINUTE / QPM_LIMIT) * 5

    # 注册天气发送任务
    count = 0
    for i, user in enumerate(crud.get_active_users(db)):
        user_cur_hour = DateUtil.get_cur_hour(user.time_zone)
        if user_cur_hour not in user.sub_hours:
            continue

        job = scheduler.add_job(
            CronJobsExecutor.send_weather,
            args=(user.chat_id, user_cur_hour),
            trigger="date",
            run_date=datetime.now(pytz.utc) + timedelta(milliseconds=i * mil_seconds_interval),
            misfire_grace_time=None
        )
        count += 1
        logger.info(f"[cron]{job}")

    return {"total": count}
