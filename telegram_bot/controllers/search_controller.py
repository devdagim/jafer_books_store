# aiogram
from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultsButton,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link


# project
from telegram_bot.bot_instance import Bot
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.models.review_model import ReviewModel
from telegram_bot.template.telegram_channel_book_post import (
    CHANNEL_POST_BODY,
    IN_STOCK_TEXT,
    OUT_OF_STOCK_TEXT,
    ORDER_NOW_BTN_TEXT,
    ADD_TO_WISHLIST_BTN_TEXT,
    REVIEWS_BTN_TEXT,
)


class SearchController:
    book_model = BookModel()
    category_model = CategoryModel()
    review_model = ReviewModel()

    async def send_search_results(self, inline_q):
        search_term, search_by = self._parse_query(inline_q)
        matches = self.book_model.search_books(search_term, search_by)

        if matches:
            query_results = []
            for book in matches:
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
        inline_btn_builder = InlineKeyboardBuilder()

        order_now_btn_link = await create_start_link(
            bot=Bot,
            payload=f"order_now_btn&book_code={book_code}",
            encode=True,
        )
        order_now_btn = InlineKeyboardButton(
            text=ORDER_NOW_BTN_TEXT, url=order_now_btn_link
        )

        add_to_wishlist_btn_link = await create_start_link(
            bot=Bot, payload=f"wishlist_btn&book_code={book_code}", encode=True
        )
        add_to_wishlist_btn = InlineKeyboardButton(
            text=ADD_TO_WISHLIST_BTN_TEXT, url=add_to_wishlist_btn_link
        )

        reviews_btn_link = await create_start_link(
            bot=Bot, payload=f"reviews_btn&book_code={book_code}", encode=True
        )
        reviews_btn = InlineKeyboardButton(
            text=REVIEWS_BTN_TEXT, url=reviews_btn_link
        )

        inline_btn_builder.add(order_now_btn, add_to_wishlist_btn)
        inline_btn_builder.add(reviews_btn)
        inline_btn_builder.adjust(2)

        return inline_btn_builder.as_markup()

    def _parse_query(self, inline_q):
        query = inline_q.query.strip("").lower()

        search_by = "all"
        search_term = query
        if query.startswith("title:"):
            search_by = "title"
            search_term = query.split("title:")[-1]
        elif query.startswith("author:"):
            search_by = "author"
            search_term = query.split("author:")[-1]

        return (search_term.strip(), search_by)
