from aiogram import Bot
from telegram_bot.helpers.config import CONFIG

# telegram bot api token
token = CONFIG.get('telegram_api','BOT_TOKEN').strip('"')

Bot = Bot(token=token,parse_mode="html")