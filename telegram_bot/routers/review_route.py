# aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject


# project
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.filter import BotDeepLink
from telegram_bot.helpers.executor import Execute


review_router = Router(name="REVIEW ROUTER")


review_router.message.middleware(
    ChannelJoinedMiddleware(["deep_link::reviews_btn&book_code={str}"])
)

@review_router.message(
    CommandStart(deep_link=True,deep_link_encoded=True),
    BotDeepLink("reviews_btn&book_code={str}"),
)
async def book_reviews_handler(message: Message, command: CommandObject):
    deep_link = command.args
    book_code = deep_link.split("=")[-1]

    await Execute(
        "controllers.review_controller",
        "ReviewController@send_first_review_page",
        message=message,
        book_code=book_code,
    ).exc()


@review_router.callback_query(F.data.startswith("review_page:"))
async def review_pagination_handler(query: CallbackQuery):
    requested_page = query.data.split(":")[1]
    book_code = query.data.split(":")[2]

    await Execute(
        "controllers.review_controller",
        "ReviewController@send_requested_review_page",
        query=query,
        book_code=book_code,
        req_page=int(requested_page),
    ).exc()
