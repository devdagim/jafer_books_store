# aiogram
from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultsButton,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# project
from telegram_bot.helpers.config import CONFIG
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.models.review_model import ReviewModel
from telegram_bot.models.post_model import PostModel
from telegram_bot.template.telegram_channel_book_post import (
    CHANNEL_POST_BODY,
    IN_STOCK_TEXT,
    OUT_OF_STOCK_TEXT,
)


class SearchController:
    book_model = BookModel()
    category_model = CategoryModel()
    review_model = ReviewModel()
    post_model = PostModel()

    async def send_search_results(self, inline_q):
        search_term = inline_q.query.strip().lower()
        search_matched_books = self.book_model.search_books(search_term)

        query_results = []

        if search_matched_books:
            for book in search_matched_books:
                book_category = self.category_model.get_book_category(
                    book["book_category"]
                )
                book_description = (
                    "By: {author_name}\nGenre: {category_name}".format(
                        author_name=book["book_author"],
                        category_name=book_category,
                    )
                )

                input_message_content = InputTextMessageContent(
                    message_text=self._input_message(selected_book=book),
                    parse_mode="html",
                )

                input_message_inline_btn = (
                    await self._input_message_inline_btn(book["book_code"])
                )

                query_results.append(
                    InlineQueryResultArticle(
                        id=book["book_code"],
                        title=book["book_name"],
                        input_message_content=input_message_content,
                        reply_markup=input_message_inline_btn,
                        description=book_description,
                        thumbnail_url=book["book_img_url"],
                        thumbnail_width=150,
                        thumbnail_height=150,
                    )
                )

        if query_results:
            inline_q_header_btn = InlineQueryResultsButton(
                text="visit our Channel for more",
                start_parameter="visit_channel",
            )

            await inline_q.answer(
                results=query_results, button=inline_q_header_btn
            )

    def _input_message(self, selected_book):
        # category name
        category_name = self.category_model.get_book_category(
            selected_book["book_category"]
        )

        # book stock status logic
        book_stock_status = selected_book["book_stoke_status"]
        if int(book_stock_status) == 1:
            stock_status = IN_STOCK_TEXT
        else:
            stock_status = OUT_OF_STOCK_TEXT

        # book rating
        book_total_rating = self.review_model.book_avg_rating(
            selected_book["book_code"]
        )
        book_total_rating = book_total_rating if book_total_rating else 0

        # generating hashtag
        category_name_parts = category_name.split(",")
        hashtag_category_names = ""
        for category_name_part in category_name_parts:
            # formatted like {#main_category #sub_category}
            hashtag_category_names += (
                "#" + category_name_part.strip().replace(" ", "_") + " "
            )

        hashtag_book_name = selected_book["book_name"].replace(" ", "_")
        hashtag_author_name = selected_book["book_author"].replace(" ", "_")

        message_content = CHANNEL_POST_BODY.format(
            book_title=selected_book["book_name"],
            author_name=selected_book["book_author"],
            category_name=category_name,
            book_language=selected_book["book_language"],
            book_etb_price=selected_book["book_etb_price"],
            book_usd_price=selected_book["book_usd_price"],
            book_stock_status=stock_status,
            book_total_rating=book_total_rating,
            hashtag_category_names=hashtag_category_names,
            hashtag_book_name=hashtag_book_name,
            hashtag_author_name=hashtag_author_name,
            book_img_url=selected_book["book_img_url"],
        )

        return message_content

    async def _input_message_inline_btn(self, book_code):
        btn_builder = InlineKeyboardBuilder()

        post_id = self.post_model.get_post_id(book_code)
        channel_username = CONFIG.get(
            "telegram_api", "CHANNEL_USERNAME"
        ).strip('"').lstrip("@")

        post_link = f"https://t.me/{channel_username}/"
        if post_id:
            post_link += post_id

        view_detail = InlineKeyboardButton(text="View Detail", url=post_link)

        btn_builder.add(view_detail)

        return btn_builder.as_markup()
