# aiogram
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery

# project
from telegram_bot.helpers.executor import Execute
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.filter import BotDeepLink

wishlist_router = Router(name="WISHLIST ROUTE")

wishlist_router.message.middleware(
    ChannelJoinedMiddleware(["wishlist_btn&book_code={str}"])
)


@wishlist_router.message(
    CommandStart(deep_link=True,deep_link_encoded=True),
    BotDeepLink("wishlist_btn&book_code={str}"),
)
async def add_to_wishlist_handler(message: Message, command: CommandObject):
    deep_link = command.args
    book_code = deep_link.split("=")[-1]
    user_id = message.from_user.id

    await Execute(
        "controllers.wishlist_controller",
        "WishlistController@add_to_wishlist",
        user_id=user_id,
        book_code=book_code,
        message=message,
    ).exc()


@wishlist_router.message(Command("wishlist"))
async def wishlist_cmd_handler(message: Message):
    await Execute(
        "controllers.wishlist_controller",
        "WishlistController@send_first_wishlist_page",
        message=message,
    ).exc()


@wishlist_router.callback_query(F.data.startswith("wishlist_page:"))
async def wishlist_pagination_handler(query: CallbackQuery):
    requested_page = query.data.split(":")[-1]

    await Execute(
        "controllers.wishlist_controller",
        "WishlistController@send_requested_wishlist_page",
        query=query,
        requested_page=int(requested_page),
    ).exc()


@wishlist_router.message(
    CommandStart(deep_link=True, deep_link_encoded=True),
    BotDeepLink("remove_wishlist&book_code={str}"),
)
async def remove_wishlist_handler(
    query: CallbackQuery, command: CommandObject
):
    book_code = command.args.split("=")[-1]

    await Execute(
        "controllers.wishlist_controller",
        "WishlistController@remove_from_wishlist",
        query=query,
        book_code=book_code,
    ).exc()
