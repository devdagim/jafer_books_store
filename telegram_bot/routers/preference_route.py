# aiogram
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery


# project
from telegram_bot.helpers.executor import Execute
from telegram_bot.models.preference_model import PreferenceModel

preference_router = Router(name="Book Preference Route")


@preference_router.message(Command("preference"))
async def preference_cmd_handler(message: Message):
    await Execute(
        "controllers.preference_controller",
        "PreferenceController@send_first_author_pref_page",
        message=message,
    ).exc()


@preference_router.callback_query(F.data.startswith("author_pref_page:"))
async def author_pref_page_handler(query: CallbackQuery):
    requested_page = query.data.split(":")[-1]

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@send_requested_author_pref_page",
        query=query,
        requested_page=int(requested_page),
    ).exc()


@preference_router.callback_query(F.data.startswith("add_author_to_pref:"))
async def add_author_handler(query: CallbackQuery):
    author_tempo_id = query.data.split(":")[1].strip()
    page_num = query.data.split(":")[2].strip()

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@add_author_to_pref",
        query=query,
        author_tempo_id=int(author_tempo_id),
        page_num=int(page_num),
    ).exc()


@preference_router.callback_query(
    F.data.startswith("remove_author_from_pref:")
)
async def remove_author_handler(query: CallbackQuery):
    author_tempo_id = query.data.split(":")[1].strip()
    page_num = query.data.split(":")[2].strip()

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@remove_author_from_pref",
        query=query,
        author_tempo_id=int(author_tempo_id),
        page_num=int(page_num),
    ).exc()


@preference_router.callback_query(F.data == "preference_form_step:genre")
async def genre_pref_page_handler(query: CallbackQuery):
    await Execute(
        "controllers.preference_controller",
        "PreferenceController@send_first_genre_pref_page",
        query=query,
    ).exc()


@preference_router.callback_query(F.data.startswith("genre_pref_page:"))
async def author_pref_page_handler(query: CallbackQuery):
    requested_page = query.data.split(":")[-1]

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@send_requested_genre_pref_page",
        query=query,
        requested_page=int(requested_page),
    ).exc()


@preference_router.callback_query(F.data.startswith("add_genre_to_pref:"))
async def add_genre_handler(query: CallbackQuery):
    category_id = query.data.split(":")[1].strip()
    page_num = query.data.split(":")[2].strip()

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@add_genre_to_pref",
        query=query,
        category_id=int(category_id),
        page_num=int(page_num),
    ).exc()


@preference_router.callback_query(F.data.startswith("remove_genre_from_pref:"))
async def remove_genre_handler(query: CallbackQuery):
    category_id = query.data.split(":")[1].strip()
    page_num = query.data.split(":")[2].strip()

    await Execute(
        "controllers.preference_controller",
        "PreferenceController@remove_genre_from_pref",
        query=query,
        category_id=int(category_id),
        page_num=int(page_num),
    ).exc()


@preference_router.callback_query(F.data == "preference_form_step:submit")
async def genre_pref_page_handler(query: CallbackQuery):
    user_id = str(query.from_user.id)
    preference_model = PreferenceModel()
    is_filled_genre_pref_form = preference_model.is_set_preference(
        user_id, preference_type="genre"
    )

    if is_filled_genre_pref_form:
        await query.message.reply(
            text="""
            Your book preferences are received. Our bot will curate personalized recommendations just for you.

            You can retrieve your book recommendations anytime 
            by typing /recommendation
            """
        )
    else:
        await query.answer(
            text="⚠️ Please choose your preferred book genre before proceeding to the next step!",
            show_alert=True,
        )


# preference_form_step:submit
