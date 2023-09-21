# aiogram
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# project
from telegram_bot.template.review_form_message import (
    RATING_FORM_HEADER,
    REVIEW_COMMENTING_FORM_HEADER,
)
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.review_model import ReviewModel


class ReviewFormController:
    book_model = BookModel()
    review_model = ReviewModel()

    async def send_rating_form(self, message, book_code):
        form_header = RATING_FORM_HEADER.format(
            book_name=(self.book_model.get_book(book_code))["book_name"]
        )

        await message.reply(
            text=form_header,
            reply_markup=self._rating_form_inline_btn(),
            parse_mode="html",
        )

    async def send_review_commenting_form(
        self, query: CallbackQuery, book_code
    ):
        form_header = REVIEW_COMMENTING_FORM_HEADER.format(
            book_name=(self.book_model.get_book(book_code))["book_name"]
        )

        await query.message.edit_text(
            text=form_header,
            inline_message_id=query.inline_message_id,
            parse_mode="html",
        )

    async def save_review(
        self, book_code, rating, user_id, message=None, state=None
    ):
        # save on giving review comment
        if message:
            review = message.text.strip("")

            error_text = self._check_review(
                review=review, entities_in_review=message.entities
            )

            if error_text:
                await message.reply(text=error_text, parse_mode="html")
            else:
                self.review_model.save_review(
                    book_code=book_code,
                    user_id=user_id,
                    rating=rating,
                    review=review,
                )

                await message.reply(
                    text="""
                    You have successfully submitted your review.
                    Thank you for sharing your feedback and for rating the book!
                    """
                )

                await state.clear()

        else:
            # save review on /cancel review commenting
            self.review_model.save_review(
                book_code=book_code, user_id=user_id, rating=rating
            )

    def _check_review(self, review, entities_in_review) -> str | None:
        error_text = None

        if entities_in_review:
            error_text = """
            <b>Error: Only text characters are allowed.</b>\nPlease don't use any commands, URLs, or any entities, just pure text.
            """

        elif len(review) > 250:
            error_text = """
            <b>Error: Review exceeded the limit.</b>\nPlease keep your review within 250 characters for a concise summary.
            """

        return error_text

    def _rating_form_inline_btn(self):
        btn_builder = InlineKeyboardBuilder()
        buttons = [
            InlineKeyboardButton(
                text="⭐️⭐️⭐️⭐️⭐️(5/5)", callback_data="rating_form_input:5"
            ),
            InlineKeyboardButton(
                text="⭐️⭐️⭐️⭐️(4/5)", callback_data="rating_form_input:4"
            ),
            InlineKeyboardButton(
                text="⭐️⭐️⭐️(3/5)", callback_data="rating_form_input:3"
            ),
            InlineKeyboardButton(
                text="⭐️⭐️(2/5)", callback_data="rating_form_input:2"
            ),
            InlineKeyboardButton(
                text="⭐️(1/5)", callback_data="rating_form_input:1"
            ),
        ]
        btn_builder.add(*buttons)
        btn_builder.adjust(1, 2, 2)

        return btn_builder.as_markup()
