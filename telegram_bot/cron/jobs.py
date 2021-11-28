from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from telegram_bot.cron import scheduler
from telegram_bot.cron.biz_weather import cron_send_weather, cron_send_warning
from telegram_bot.database import crud
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.utils.date_util import DateUtil

QPM_LIMIT = 500
ONE_MINUTE = 60 * 1000
# 限流: https://dev.qweather.com/docs/start/glossary#qpm
MIL_SECONDS_INTERVAL = (ONE_MINUTE / QPM_LIMIT) * 5
# 天气预警触发
VALID_WARNING_CHECK_HOURS = (6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22)

router = APIRouter()


async def send_weather_by_user(user_id: str, user_cur_hour: str):
    logger.info(f"[send_weather_by_user]start,{user_id},{user_cur_hour}")
    with get_db_session() as db:
        chat = crud.get_user(db, user_id)
    if not chat or not chat.is_active:
        return {"message": "USER_NOT_FOUND"}

    return await cron_send_weather(chat)


@router.get("/cron")
async def cron_handler(db: Session = Depends(get_db)):
    """ 外部请求触发的定时任务，每个小时执行一次 """
    count = 0
    for i, user in enumerate(crud.get_active_users(db)):
        run_date = datetime.now(pytz.utc) + timedelta(milliseconds=i * MIL_SECONDS_INTERVAL)

        # 天气发送任务注册
        cur_hour = DateUtil.get_cur_hour(user.time_zone)
        if cur_hour not in user.sub_hours:
            continue

        job = scheduler.add_job(
            send_weather_by_user,
            args=(user.chat_id, cur_hour),
            trigger="date",
            run_date=run_date,
            misfire_grace_time=None
        )
        count += 1
        logger.info(f"[cron][add_job][send_weather]{job}")

    return {"total": count}


# 自然灾害预警信息获取
async def send_warning_by_user(user_id: str):
    logger.info(f"[send_warning_by_user]start,{user_id}")
    with get_db_session() as db:
        chat = crud.get_user(db, user_id)
    if not chat or not chat.is_active:
        return {"message": "USER_NOT_FOUND"}

    return await cron_send_warning(chat)


@router.get("/cron_1h")
async def one_hour_cron_handler(db: Session = Depends(get_db)):
    """ 外部请求触发的定时任务，每个小时执行一次 """
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if now.hour not in VALID_WARNING_CHECK_HOURS:
        return {"total": 0}

    count = 0
    for i, user in enumerate(crud.get_active_users(db)):
        run_date = now + timedelta(milliseconds=i * MIL_SECONDS_INTERVAL)

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
