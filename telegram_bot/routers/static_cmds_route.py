# aiogram
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


# project
from telegram_bot.helpers.executor import Execute
from telegram_bot.helpers.config import CONFIG
from telegram_bot.middleware import ChannelJoinedMiddleware
import telegram_bot.template.static_cmds_message as MessageTemplate

static_cmds_router = Router(name="static cmds route")


static_cmds_router.message.middleware(
    ChannelJoinedMiddleware(["command::start"])
)

# ? done
@static_cmds_router.message(
    CommandStart(deep_link=True), F.text == "/start visit_channel"
)
async def visit_channel_handler(message: Message):
    channel_username = (
        CONFIG.get("telegram_api", "CHANNEL_USERNAME").strip('"').strip("@")
    )
    msg_body = f"https://t.me/{channel_username}"

    await message.answer(text=msg_body)


@static_cmds_router.message(Command("start"))
async def start_handler(message: Message):
    await Execute(
        "controllers.start_controller",
        "StartController@start_the_bot",
        message=message
    ).exc()

# ? done
@static_cmds_router.message(Command("search"))
async def search_handler(message: Message):
    bot_username = CONFIG.get("telegram_api", "BOT_USERNAME").strip('"')
    msg_body = MessageTemplate.Search_Guide.format(bot_username=bot_username)

    await message.answer(text=msg_body, parse_mode="html")

# ? done
@static_cmds_router.message(Command("contact"))
async def contact_handler(message: Message):
    msg_body = MessageTemplate.Contact

    await message.answer(
        text=msg_body, parse_mode="html", disable_web_page_preview=True
    )
