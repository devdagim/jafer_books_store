# aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

# project
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.helpers.executor import Execute


recommendation_router = Router(name="recommendation route")


recommendation_router.message.middleware(
    ChannelJoinedMiddleware(["command::recommendation"])
)


@recommendation_router.message(Command("recommendation"))
async def wishlist_cmd_handler(message: Message):
    await Execute(
        "controllers.recommendation_controller",
        "RecommendationController@send_first_recommendation_page",
        message=message,
    ).exc()


@recommendation_router.callback_query(
    F.data.startswith("recommendation_page:")
)
async def wishlist_pagination_handler(query: CallbackQuery):
    requested_page = query.data.split(":")[-1]

    await Execute(
        "controllers.recommendation_controller",
        "RecommendationController@send_requested_recommendation_page",
        query=query,
        requested_page=int(requested_page),
    ).exc()
