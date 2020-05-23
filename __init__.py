# -*- coding: utf-8 -*-

# Initial bot by Telegram access token
import os

import telegram

bot = telegram.Bot(token=(os.environ['ACCESS_TOKEN']))
chat_ids = os.environ["CHAT_IDS"].split(',')
