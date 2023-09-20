# aiogram
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# project
from telegram_bot.filter import BotDeepLink
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.helpers.executor import Execute

order_router = Router(name="ORDER_ROUTE")

# format of order_now btn /start?order_now_btn&book_code={book_code}
# located in channel post as inline btn
order_router.message.middleware(
    ChannelJoinedMiddleware(["order_now_btn&book_code={str}"])
)


class OrderState(StatesGroup):
    order_method = State()


@order_router.message(
    CommandStart(deep_link=True,deep_link_encoded=True),
    BotDeepLink("order_now_btn&book_code={str}"),
)
async def order_btn_handler(
    message: Message, command: CommandObject, state: FSMContext
):
    deep_link = command.args
    book_code = deep_link.split("=")[-1]

    # set state and data
    await state.set_state(OrderState.order_method)
    await state.set_data({"book_code": book_code})
    # send order options
    await Execute(
        "controllers.order_controller",
        "OrderController@send_order_options",
        message=message,
    ).exc()


@order_router.callback_query(
    OrderState.order_method, F.data.startswith("order_option:")
)
async def order_option_inline_btn_handler(
    query: CallbackQuery, state: FSMContext
):
    data = {
        "order_option": query.data.split("order_option:")[-1],
        "book_code": (await state.get_data())["book_code"],
    }

    await Execute(
        "controllers.order_controller",
        "OrderController@send_selected_order_option",
        query=query,
        data=data,
    ).exc()

    await state.clear()
