# aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

# project
from telegram_bot.filter import BotDeepLink
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.helpers.executor import Execute

order_router = Router(name="ORDER_ROUTE")

order_router.message.middleware(
    ChannelJoinedMiddleware(["deep_link::order_now_btn&book_code={str}"])
)


@order_router.message(
    CommandStart(deep_link=True, deep_link_encoded=True),
    BotDeepLink("order_now_btn&book_code={str}"),
)
async def order_btn_handler(
    message: Message, command: CommandObject, state: FSMContext
):
    deep_link = command.args
    book_code = deep_link.split("=")[-1]

    # set  data
    await state.set_data({"book_code": book_code})
    # send order options
    await Execute(
        "controllers.order_controller",
        "OrderController@send_order_options",
        message=message,
    ).exc()


@order_router.callback_query(F.data.startswith("order_option:"))
async def order_option_inline_btn_handler(
    query: CallbackQuery, state: FSMContext
):
    session_data = await state.get_data()

    if session_data["book_code"]:
        order_option = query.data.split("order_option:")[-1]
        book_code = session_data["book_code"]

        await Execute(
            "controllers.order_controller",
            "OrderController@send_selected_order_option",
            query=query,
            book_code=book_code,
            order_option=int(order_option),
        ).exc()

        await state.clear()
