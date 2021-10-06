from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from telegram_bot.database import crud
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.scheduler import scheduler
from telegram_bot.scheduler.jobs import send_warning_by_user, send_weather_by_user
from telegram_bot.util.date_util import DateUtil

QPM_LIMIT = 500
ONE_MINUTE = 60 * 1000
# 限流: https://dev.qweather.com/docs/start/glossary#qpm
MIL_SECONDS_INTERVAL = (ONE_MINUTE / QPM_LIMIT) * 5

VALID_WARNING_CHECK_HOURS = (6, 8, 10, 12, 14, 16, 18, 20, 22, 24)

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
    """ 外部请求触发的定时任务，每个小时执行一次 """
    count = 0
    for i, user in enumerate(crud.get_active_users(db)):
        run_date = datetime.now(pytz.utc) + timedelta(milliseconds=i * MIL_SECONDS_INTERVAL)

        # 天气发送任务注册
        user_cur_hour = DateUtil.get_cur_hour(user.time_zone)
        if user_cur_hour not in user.sub_hours:
            continue

        job = scheduler.add_job(
            send_weather_by_user,
            args=(user.chat_id, user_cur_hour),
            trigger="date",
            run_date=run_date,
            misfire_grace_time=None
        )
        count += 1
        logger.info(f"[cron][add_job][send_weather]{job}")

    return {"total": count}


@router.get("/cron_1h")
async def one_hour_cron_handler(db: Session = Depends(get_db)):
    """ 外部请求触发的定时任务，每个小时执行一次 """
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour not in VALID_WARNING_CHECK_HOURS:
        return {"total": 0}

    count = 0
    for i, user in enumerate(crud.get_active_users(db)):
        run_date = now + timedelta(milliseconds=i * MIL_SECONDS_INTERVAL)

        # 自然灾害预警信息获取
        job = scheduler.add_job(
            send_warning_by_user,
            args=(user.chat_id,),
            trigger="date",
            run_date=run_date,
            misfire_grace_time=None
        )
        count += 1
        logger.info(f"[cron][add_job][send_warning]{job}")

    return {"total": count}
