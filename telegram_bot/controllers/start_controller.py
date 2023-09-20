# aiogram
from aiogram.types import Message, BotCommand

# project
from telegram_bot.template.static_cmds_message import Welcome


class StartController:
    async def start_the_bot(self, message: Message):
        user_name = message.from_user.first_name
        bot_name = (await message.bot.me()).username

        msg_body = Welcome.format(
            user_name=user_name,
            bot_name=bot_name,
        )

        await message.answer(text=msg_body, parse_mode="html")
