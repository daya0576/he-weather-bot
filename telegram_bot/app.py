# -*- coding: utf-8 -*-
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from telegram_bot.database import models
from telegram_bot.database.database import engine
from telegram_bot.routers import webhook, cron
from telegram_bot.settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(webhook.router)
app.include_router(cron.router)

if settings.SENTRY_URL:
    sentry_sdk.init(dsn="https://22cf74145c784a35b0f5ce69b9df2bf2@o527049.ingest.sentry.io/5642886")
    app = SentryAsgiMiddleware(app)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
