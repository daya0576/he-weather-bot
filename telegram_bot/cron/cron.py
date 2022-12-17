from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from telegram_bot.cron import scheduler
from telegram_bot.cron.tasks import cron_send_weather, cron_send_warning
from telegram_bot.database import crud
from telegram_bot.database.database import get_db
from telegram_bot.utils.date_util import DateUtil

QPM_LIMIT = 100 * 1.5
ONE_MINUTE = 60 * 1000
API_COUNT = 5
# 限流: https://dev.qweather.com/docs/start/glossary#qpm
MIL_SECONDS_INTERVAL = ONE_MINUTE / (QPM_LIMIT * API_COUNT)
# 天气预警触发
VALID_WARNING_CHECK_HOURS = (0, 6, 9, 12, 15, 18, 21)

router = APIRouter()


@router.get("/cron")
async def cron_handler(db: Session = Depends(get_db)):
    """外部请求触发的定时任务，每个小时执行一次"""
    count = 0
    for i, chat in enumerate(crud.get_active_users(db)):
        run_date = datetime.now(pytz.utc) + timedelta(
            milliseconds=i * MIL_SECONDS_INTERVAL
        )

        # 用户定时订阅判断逻辑
        cur_hour = str(DateUtil.get_cur_hour(chat.time_zone))
        if cur_hour not in chat.sub_hours:
            continue

        job = scheduler.add_job(
            cron_send_weather,
            args=(chat, chat.ding_bot),
            trigger="date",
            run_date=run_date,
            misfire_grace_time=None,
        )
        count += 1
        logger.info(f"[cron][add_job][send_weather]{job}")

    return {"total": count}


@router.get("/cron_1h")
async def one_hour_cron_handler(db: Session = Depends(get_db)):
    """每个小时执行一次，自然灾害预警信息获取"""
    now = datetime.now(pytz.timezone("Asia/Shanghai"))
    if now.hour not in VALID_WARNING_CHECK_HOURS:
        return {"total": 0}

    count = 0
    for i, chat in enumerate(crud.get_active_users(db)):
        run_date = now + timedelta(milliseconds=i * MIL_SECONDS_INTERVAL)

        job = scheduler.add_job(
            cron_send_warning,
            args=(chat, chat.ding_bot),
            trigger="date",
            run_date=run_date,
            misfire_grace_time=None,
        )
        count += 1
        logger.info(f"[cron][add_job][send_warning]{job}")

    return {"total": count}
