# python
from math import ceil

# aiogram
from aiogram import exceptions
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link

# project
from telegram_bot.bot_instance import Bot
from telegram_bot.models.review_model import ReviewModel
from telegram_bot.models.book_model import BookModel
from telegram_bot.template.review_message import (
    BOOK_REVIEWS_HEADER,
    REVIEW_BODY,
    EMPTY_REVIEW_BODY,
)


class ReviewController:
    review_model = ReviewModel()
    book_model = BookModel()

    async def send_first_review_page(self, message, book_code):
        header = self._review_header(book_code)
        body = await self._review_body(book_code, 1)
        pagination_btn = await self._inline_pagination_btn(book_code, 1)

        if not body:
            body = EMPTY_REVIEW_BODY

        # header
        await message.answer(text=header, parse_mode="html")
        # review body
        await message.answer(
            text=body, reply_markup=pagination_btn, parse_mode="html"
        )

    async def send_requested_review_page(self, query, book_code, req_page):
        body = await self._review_body(book_code, req_page)
        pagination_btn = await self._inline_pagination_btn(book_code, req_page)

        await query.message.edit_text(
            text=body,
            inline_message_id=query.inline_message_id,
            reply_markup=pagination_btn,
            parse_mode="html",
        )

    def _review_header(self, book_code):
        average_rating = self.review_model.book_avg_rating(book_code)
        book = self.book_model.get_book(book_code)

        review_msg_header = BOOK_REVIEWS_HEADER.format(
            book_name=book["book_name"],
            average_rating=average_rating,
        )

        return review_msg_header

    async def _review_body(self, book_code, current_review_page):
        review_per_page = 3
        limit_start = (current_review_page - 1) * review_per_page
        fetch_limit = (limit_start, review_per_page)

        review_msg_body = ""
        book_reviews = self.review_model.get_reviews(book_code, fetch_limit)

        if book_reviews:
            for i, book_review in enumerate(book_reviews, start=1):
                rating_star = ""
                for _ in range(int(book_review["rating"])):
                    rating_star += "⭐️"

                reviewer_id = book_review["user_id"]
                reviewer_name = ""
                review = (
                    "💬 " + book_review["review"]
                    if book_review["review"]
                    else " "
                )

                try:
                    reviewer_name = (
                        await Bot.get_chat(chat_id=reviewer_id)
                    ).full_name
                except exceptions.TelegramBadRequest as e:
                    reviewer_name = "Anonymous user"

                review_msg_body += REVIEW_BODY.format(
                    review_num=i + ((current_review_page - 1) * 3),
                    reviewer_id=reviewer_id,
                    reviewer_name=reviewer_name,
                    rating_star=rating_star,
                    rating=int(book_review["rating"]),
                    review_date=(book_review["create_time"]).strftime(
                        "%d/%m/%Y"
                    ),
                    review=review,
                )

        return review_msg_body

    async def _inline_pagination_btn(self, book_code, current_review_page):
        review_per_page = 3
        total_reviews = self.review_model.total_reviews(book_code)
        total_review_pages = ceil(total_reviews / review_per_page)

        back_page = current_review_page - 1
        next_page = current_review_page + 1

        btn_builder = InlineKeyboardBuilder()

        review_btn_link = await create_start_link(
            bot=Bot, payload=f"write_review&book_code={book_code}", encode=True
        )
        review_btn = InlineKeyboardButton(
            text="Write Review",
            url=review_btn_link,
        )
        btn_builder.add(review_btn)

        if total_reviews > review_per_page:
            back_btn = InlineKeyboardButton(
                text="⏪  back",
                callback_data=f"review_page:{back_page}:{book_code}",
            )
            next_btn = InlineKeyboardButton(
                text="⏩  next",
                callback_data=f"review_page:{next_page}:{book_code}",
            )

            if next_page > total_review_pages:
                buttons = [back_btn]
            elif back_page == 0:
                buttons = [next_btn]
            else:
                buttons = [back_btn, next_btn]
            btn_builder.add(*buttons)

        btn_builder.adjust(1, 2)

        return btn_builder.as_markup()
