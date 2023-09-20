# aiogram
from aiogram import Router
from aiogram.types import InlineQuery


# project
from telegram_bot.helpers.executor import Execute


search_router = Router(name="SEARCH ROUTER")


@search_router.inline_query()
async def inline_query_handler(inline_q: InlineQuery):
    await Execute(
        "controllers.search_controller",
        "SearchController@send_search_results",
        inline_q=inline_q,
    ).exc()
