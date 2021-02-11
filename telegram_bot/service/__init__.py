# -*- coding: utf-8 -*-
from telegram_bot.intergration import he_weather
from telegram_bot.service.message_service import MessageService

message_service = MessageService(he_weather)
