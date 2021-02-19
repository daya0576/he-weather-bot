# -*- coding: utf-8 -*-
import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from telegram_bot.database import models
from telegram_bot.database.database import engine
from telegram_bot.routers import webhook, cron
from telegram_bot.settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(webhook.router)
app.include_router(cron.router)

# sentry middleware
if settings.SENTRY_URL:
    sentry_sdk.init(dsn=settings.SENTRY_URL)
    app = SentryAsgiMiddleware(app)

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
else:
    logger.setLevel(logging.INFO)
