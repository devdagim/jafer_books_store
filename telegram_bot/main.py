# fastapi module
from fastapi import FastAPI
import uvicorn

# test module
import ngrok
import logging

# aiogram module
from aiogram import Dispatcher
from aiogram.types import Update, BotCommand

# project module
from telegram_bot.helpers.aiomysql_storage import AioMysqlStorage
from telegram_bot.bot_instance import Bot
from telegram_bot.routers import Routers
from telegram_bot.helpers.config import CONFIG

logging.basicConfig(level=logging.INFO)

# telegram bot api token
token = CONFIG.get("telegram_api", "BOT_TOKEN").strip('"')
# ngrok tunnel url generator
tunnel = ngrok.connect(5050)


# telegram server sending it update to this path
webhook_path = f"/bot/{token}"
webhook_url = tunnel.url() + webhook_path

dp = Dispatcher(storage=AioMysqlStorage())
dp.include_routers(*Routers)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    webhook_info = await Bot.get_webhook_info()
    # commands = [
    #     BotCommand(
    #         command="/preference",
    #         description="✅ Set your preferences for personalized book recommendations",
    #     ),
    #     BotCommand(
    #         command="/recommendation",
    #         description="📚 Get personalized book suggestions",
    #     ),
    #     BotCommand(command="/wishlist", description="📌 Manage your wishlist"),
    #     BotCommand(command="/search", description="🔎 Search for books"),
    #     BotCommand(command="/contact", description="📞 To get contact info"),
    # ]

    if webhook_info.url != webhook_url:
        await Bot.set_webhook(url=webhook_url)

    # await Bot.set_my_commands(commands=commands)


@app.post(webhook_path)
async def feed_update(update: dict):
    telegram_update = Update(**update)
    await dp.feed_webhook_update(bot=Bot, update=telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await Bot.delete_webhook(drop_pending_updates=True)
    await Bot.session.close()


if __name__ == "__main__":
    uvicorn.run(app, port=5050)
