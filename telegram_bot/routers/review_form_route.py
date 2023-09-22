# aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


# project
from telegram_bot.middleware import ChannelJoinedMiddleware
from telegram_bot.filter import BotDeepLink
from telegram_bot.helpers.executor import Execute


review_form_router = Router(name="REVIEW FORM ROUTER")
review_form_state_router = Router(name="REVIEW FORM state ROUTER")


review_form_router.message.middleware(
    ChannelJoinedMiddleware(["deep_link::write_review&book_code={str}"])
)

class ReviewFormState(StatesGroup):
    review_cmt = State()


@review_form_router.message(
    CommandStart(deep_link=True, deep_link_encoded=True),
    BotDeepLink("write_review&book_code={str}"),
)
async def write_review_handler(
    message: Message, command: CommandObject, state: FSMContext
):
    deep_link = command.args
    book_code = deep_link.split("=")[-1]
    await state.set_data({"book_code": book_code})

    await Execute(
        "controllers.review_form_controller",
        "ReviewFormController@send_rating_form",
        message=message,
        book_code=book_code,
    ).exc()


@review_form_router.callback_query(F.data.startswith("rating_form_input:"))
async def rating_handler(query: CallbackQuery, state: FSMContext):
    rating_point = query.data.split("rating_form_input:")[-1]
    book_code = (await state.get_data())["book_code"]

    await state.set_data({"rating_point": rating_point})
    await state.set_state(ReviewFormState.review_cmt)

    await Execute(
        "controllers.review_form_controller",
        "ReviewFormController@send_review_commenting_form",
        query=query,
        book_code=book_code,
    ).exc()


@review_form_state_router.message(
    StateFilter(ReviewFormState.review_cmt),Command("cancel"),
)
async def cancel_review_commenting(message: Message, state: FSMContext):
    data = await state.get_data()

    await Execute(
        "controllers.review_form_controller",
        "ReviewFormController@save_review",
        book_code=data["book_code"],
        rating=int(data["rating_point"]),
        user_id=message.from_user.id,
    ).exc()

    await message.reply(
        text="You have successfully submitted your review\nThank you for rating."
    )

    await state.clear()


@review_form_state_router.message(
    StateFilter(ReviewFormState.review_cmt), F.content_type == "text"
)
async def review_cmt_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await Execute(
        "controllers.review_form_controller",
        "ReviewFormController@save_review",
        book_code=data["book_code"],
        rating=int(data["rating_point"]),
        user_id=message.from_user.id,
        message=message,
        state=state,
    ).exc()
