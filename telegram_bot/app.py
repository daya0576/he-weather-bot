# -*- coding: utf-8 -*-
import sys

from fastapi import FastAPI
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import uvicorn

from telegram_bot.controllers import meta, release, webhook
from telegram_bot.cron import cron, scheduler
from telegram_bot.database import models
from telegram_bot.database.database import engine
from telegram_bot.settings import settings, aio_lru_cache_1h

# 日志格式设置
logger.remove()
FORMAT = "<level>{level: <6}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{message}</level>"
logger.add(sys.stdout, colorize=True, format=FORMAT, diagnose=False)

app = FastAPI()
app.include_router(meta.router)
app.include_router(webhook.router)
app.include_router(cron.router)
app.include_router(release.router)


@aio_lru_cache_1h
@app.on_event("startup")
async def startup_event():
    # 定时任务
    scheduler.start()
    logger.info("starting cron service..", scheduler)

    # 数据库更新
    logger.info("updating database schema..")
    models.Base.metadata.create_all(bind=engine)


# sentry middleware
if settings.SENTRY_URL:
    sentry_sdk.init(
        dsn=settings.SENTRY_URL,
        environment=settings.ENV,
        # To set a uniform sample rate
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production
        profiles_sample_rate=1.0,
    )
    app = SentryAsgiMiddleware(app)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
