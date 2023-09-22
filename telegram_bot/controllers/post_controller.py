import asyncio
from time import sleep
from math import ceil

# aiogram
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link

# project
from telegram_bot.bot_instance import Bot
from telegram_bot.helpers.config import CONFIG

# models
from telegram_bot.models.post_model import PostModel
from telegram_bot.models.review_model import ReviewModel
from telegram_bot.models.category_model import CategoryModel

# message templates
from telegram_bot.template.telegram_channel_book_post import (
    CHANNEL_POST_BODY,
    IN_STOCK_TEXT,
    OUT_OF_STOCK_TEXT,
    ORDER_NOW_BTN_TEXT,
    ADD_TO_WISHLIST_BTN_TEXT,
    REVIEWS_BTN_TEXT,
)


class PostController:
    # MODEL
    post_model = PostModel()
    review_model = ReviewModel()
    category_model = CategoryModel()

    # aiogram and Telegram bot config
    CHANNEL_USERNAME = CONFIG.get("telegram_api", "CHANNEL_USERNAME").strip(
        '"'
    )

    # main func
    # posting books to channel
    def post(self):
        # basic pagination algorithm
        # to fetch all unposted books based on limit
        post_per_round = 50  # fetch 50 rows per query
        total_book = self.post_model.unposted_books_count()
        total_round = ceil(total_book / post_per_round)

        for round_number in range(total_round):
            limit_start = round_number * post_per_round
            limit_end = (round_number + 1) * post_per_round
            fetch_limit = (limit_start, limit_end)

            # fetch unposted books
            unposted_books = self.post_model.get_unposted_books(fetch_limit)

            for book in unposted_books:
                book_code = book["book_code"]

                # generating post template from static template
                post_data = self.post_template(book)

                # sending post to channel
                loop = asyncio.get_event_loop()
                post_id = loop.run_until_complete(
                    self.send_post_to_channel(book_code, post_data)
                )

                # saving post id and changing the post status
                self.post_model.save_post(post_id, book_code)
                sleep(40)

    # main func
    # editing posts form the channel
    # on book attr updated
    def edit_post(self):
        post_per_round = 50  # fetch 50 rows per query
        total_book = self.post_model.updated_books_count()
        total_round = ceil(total_book / post_per_round)

        for round_number in range(total_round):
            limit_start = round_number * post_per_round
            limit_end = (round_number + 1) * post_per_round
            fetch_limit = (limit_start, limit_end)

            # fetch updated books
            updated_books = self.post_model.get_updated_books(fetch_limit)
            for book in updated_books:
                book_code = book["book_code"]
                post_id = book["post_id"]

                # generating post template from static template
                post_data = self.post_template(book)

                # editing post from the channel
                # for updated books
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    self.edit_post_from_channel(post_id, post_data, book_code)
                )

                # changing book content status from updated-> original
                self.post_model.update_book_content_status(book_code,0)
                sleep(40)

    # class method | aiogram.bot.send_mes..
    # send message to telegram
    async def send_post_to_channel(self, book_code, message):
        post_inline_btn = await self.post_inline_btn(book_code)

        response_msg = await Bot.send_message(
            chat_id=self.CHANNEL_USERNAME,
            text=message,
            reply_markup=post_inline_btn,
            request_timeout=120
        )

        post_id = response_msg.message_id

        return post_id  # the posted message id

        # class method

    # cls method | aiogram.bot.edit_...
    # edit message from telegram channel
    async def edit_post_from_channel(self, post_id, message, book_code):
        inline_btn = self.post_inline_btn(book_code)
        await Bot.edit_message_text(
            chat_id=self.CHANNEL_USERNAME,
            message_id=post_id,
            text=message,
            reply_markup=inline_btn,
            request_timeout=120
        )

    # class method
    # generating inline btn for the post
    async def post_inline_btn(self, book_code):
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
        inline_btn_builder.adjust(2)  # making 2X2 grid btn layout

        return inline_btn_builder.as_markup()

    # generate post template using telegram_channel_book_post template
    def post_template(self, data):
        # category name
        category_name = self.category_model.get_book_category(
            data["book_category"]
        )

        # book stock status logic
        book_stock_status = data["book_stoke_status"]
        if int(book_stock_status) == 1:
            stock_status = IN_STOCK_TEXT
        else:
            stock_status = OUT_OF_STOCK_TEXT

        # book rating
        book_total_rating = self.review_model.book_avg_rating(
            data["book_code"]
        )

        # generating hashtag
        category_name_parts = category_name.split(",")
        hashtag_category_names = ""
        for category_name_part in category_name_parts:
            # formatted like {#main_category #sub_category}
            hashtag_category_names += (
                "#" + category_name_part.strip().replace(" ", "_") + " "
            )

        hashtag_book_name = data["book_name"].replace(" ", "_")
        hashtag_author_name = data["book_author"].replace(" ", "_")

        template = CHANNEL_POST_BODY.format(
            book_title=data["book_name"],
            author_name=data["book_author"],
            category_name=category_name,
            book_language=data["book_language"],
            book_etb_price=data["book_etb_price"],
            book_usd_price=data["book_usd_price"],
            book_stock_status=stock_status,
            book_total_rating=book_total_rating,
            hashtag_category_names=hashtag_category_names,
            hashtag_book_name=hashtag_book_name,
            hashtag_author_name=hashtag_author_name,
            book_img_url=data["book_img_url"],
        )

        return template
