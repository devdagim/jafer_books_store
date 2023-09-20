from math import ceil

# aiogram
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link


# project
from telegram_bot.bot_instance import Bot
from telegram_bot.helpers.config import CONFIG
from telegram_bot.template.wishlist_message import Recommended_Book_Template
from telegram_bot.models.recommendation_model import RecommendationModel
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.post_model import PostModel
from telegram_bot.models.preference_model import PreferenceModel


class RecommendationController:
    recommendation_model = RecommendationModel()
    category_model = CategoryModel()
    book_model = BookModel()
    post_model = PostModel()

    async def send_first_recommendation_page(self, message):
        user_id = str(message.from_user.id)
        preference_model = PreferenceModel()
        is_filled_genre_pref_form = preference_model.is_set_preference(
            user_id, preference_type="genre"
        )

        if is_filled_genre_pref_form:
            body = await self._recommendation_body(
                current_list_page=1, user_id=user_id
            )
            pagination_btn = self._inline_pagination_btn(user_id, 1)

            # header
            await message.answer(
                text="""🔍 <b>Recommended Books:</b>""", parse_mode="html"
            )
            # wishlist body
            await message.answer(
                text=body,
                reply_markup=pagination_btn,
                parse_mode="html",
                disable_web_page_preview=True,
            )
        else:
            await message.answer(
                text="📚 To receive personalized book recommendations from our bot, set your book preferences by sending the command /preference",
            )

    async def send_requested_recommendation_page(self, query, requested_page):
        user_id = str(query.from_user.id)

        body = await self._recommendation_body(requested_page, user_id)
        pagination_btn = self._inline_pagination_btn(user_id, requested_page)

        # replace the recommendation body with request one
        await query.message.edit_text(
            text=body,
            inline_message_id=query.inline_message_id,
            reply_markup=pagination_btn,
            parse_mode="html",
            disable_web_page_preview=True,
        )

    async def _recommendation_body(self, current_list_page, user_id):
        list_per_page = 3
        limit_start = (current_list_page - 1) * list_per_page
        fetch_limit = (limit_start, list_per_page)

        message_body = ""
        recommend_books = self.recommendation_model.recommended_books(
            user_id, fetch_limit
        )

        if recommend_books:
            for i, recommend_book in enumerate(recommend_books, start=1):
                book_code = recommend_book["book_code"]
                book = self.book_model.get_book(book_code)

                book_category = self.category_model.get_book_category(
                    book["book_category"]
                )

                order_page_link = await create_start_link(
                    bot=Bot,
                    payload=f"order_now_btn&book_code={book_code}",
                    encode=True,
                )

                post_id = self.post_model.get_post_id(book_code)
                channel_username = (
                    CONFIG.get("telegram_api", "CHANNEL_USERNAME")
                    .strip('"')
                    .strip("@")
                )
                book_channel_post_link = (
                    f"https://t.me/{channel_username}/{post_id}"
                )

                message_body += Recommended_Book_Template.format(
                    list_number=i + ((current_list_page - 1) * 3),
                    book_name=book["book_name"],
                    book_author=book["book_author"],
                    book_category=book_category,
                    etb_price=book["book_etb_price"],
                    usd_price=book["book_usd_price"],
                    order_page_link=order_page_link,
                    book_channel_post_link=book_channel_post_link,
                )

        return message_body

    def _inline_pagination_btn(self, user_id, current_list_page):
        list_per_page = 3
        total_list = self.recommendation_model.total_recommended_books(user_id)
        total_list_pages = ceil(total_list / list_per_page)

        back_page = current_list_page - 1
        next_page = current_list_page + 1

        if total_list > list_per_page:
            back_btn = InlineKeyboardButton(
                text="⏪ back",
                callback_data=f"recommendation_page:{back_page}",
            )
            page_info_btn = InlineKeyboardButton(
                text=str(current_list_page) + "/" + str(total_list_pages),
                callback_data="disabled_btn",
            )
            next_btn = InlineKeyboardButton(
                text="next ⏩",
                callback_data=f"recommendation_page:{next_page}",
            )

            if (
                current_list_page == total_list_pages
                and current_list_page == 1
            ):
                pagination_buttons = [page_info_btn]
            elif current_list_page == 1:
                pagination_buttons = [page_info_btn, next_btn]
            elif current_list_page == total_list_pages:
                pagination_buttons = [back_btn, page_info_btn]
            else:
                pagination_buttons = [
                    back_btn,
                    page_info_btn,
                    next_btn,
                ]

            btn_builder = InlineKeyboardBuilder()
            btn_builder.add(*pagination_buttons)
            btn_markup = btn_builder.as_markup()

        return btn_markup if btn_markup else None
