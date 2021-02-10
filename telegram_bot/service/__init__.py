# -*- coding: utf-8 -*-
from telegram_bot.intergration import ascii_weather
from telegram_bot.service.message_service import MessageService

message_service = MessageService(ascii_weather)
