# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

from telegram_bot.routers import webhook, cron

app = FastAPI()
app.include_router(webhook.router)
app.include_router(cron.router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
