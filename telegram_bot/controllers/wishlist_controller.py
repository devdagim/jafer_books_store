# python
from math import ceil

# aiogram
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link


# project
from telegram_bot.bot_instance import Bot
from telegram_bot.helpers.config import CONFIG
from telegram_bot.models.wishlist_model import WishlistModel
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.template.wishlist_message import (
    SUCCESS_MESSAGE,
    Wishlist_header,
    BOOK_LIST,
    LIST_EMPTY,
    LIST_REMOVED_SUCCESS_MESSAGE,
)


class WishlistController:
    wishlist_model = WishlistModel()
    book_model = BookModel()

    async def add_to_wishlist(self, book_code, user_id, message):
        # save the book to the wishlist
        self.wishlist_model.save_to_wishlist(book_code, user_id)

        # send success message
        await self._send_success_message(book_code, message)

    async def _send_success_message(self, book_code, message):
        book_info = self.book_model.get_book(book_code)
        book_name = book_info["book_name"]

        success_msg = SUCCESS_MESSAGE.format(book_name=book_name)

        await message.reply(text=success_msg, parse_mode="html")

    async def send_first_wishlist_page(self, message: Message):
        user_id = message.from_user.id

        header = self._wishlist_header(user_id)
        body = await self._wishlist_body(1, user_id)
        pagination_btn = None

        if body:
            pagination_btn = self._inline_pagination_btn(user_id, 1)
        else:
            # empty message logic
            channel_username = CONFIG.get(
                "telegram_api", "CHANNEL_USERNAME"
            ).strip('"')
            body += LIST_EMPTY.format(channel_username=channel_username)

        # header
        await message.answer(text=header, parse_mode="html")
        # wishlist body
        await message.answer(
            text=body,
            reply_markup=pagination_btn,
            parse_mode="html",
            disable_web_page_preview=True,
        )

    async def send_requested_wishlist_page(self, query: CallbackQuery, requested_page):
        user_id = query.from_user.id

        body = await self._wishlist_body(requested_page, user_id)
        pagination_btn = self._inline_pagination_btn(user_id, requested_page)

        # replace the wishlist body with request one
        await query.message.edit_text(
            text=body,
            inline_message_id=query.inline_message_id,
            reply_markup=pagination_btn,
            parse_mode="html",
            disable_web_page_preview=True
        )

    async def remove_from_wishlist(self, query: CallbackQuery, book_code):
        user_id = query.from_user.id
        # remove from wishlist
        self.wishlist_model.remove_wishlist(user_id, book_code)

        # show success message
        book_info = self.book_model.get_book(book_code)

        success_message = LIST_REMOVED_SUCCESS_MESSAGE.format(
            book_name=book_info["book_name"],
            book_author=book_info["book_author"],
        )
        await query.answer(text=success_message, show_alert=True)

    def _wishlist_header(self, user_id: int):
        total_list = self.wishlist_model.get_total_list(user_id)

        message_header = Wishlist_header.format(total_list=total_list)

        return message_header

    async def _wishlist_body(self, current_list_page: int, user_id: int):
        category_model = CategoryModel()

        list_per_page = 3
        limit_start = (current_list_page - 1) * list_per_page
        fetch_limit = (limit_start, list_per_page)

        message_body = ""
        books_in_wishlist = self.wishlist_model.get_wishlist(
            user_id, fetch_limit
        )

        if books_in_wishlist:
            for i, book_in_wishlist in enumerate(books_in_wishlist, start=1):
                book_category = category_model.get_book_category(
                    book_in_wishlist["book_category"]
                )
                book_code = book_in_wishlist["book_code"]

                order_page_link = await create_start_link(
                    bot=Bot,
                    payload=f"order_now_btn&book_code={book_code}",
                    encode=True,
                )

                remove_from_wishlist_link = await create_start_link(
                    bot=Bot,
                    payload=f"remove_wishlist&book_code={book_code}",
                    encode=True,
                )

                message_body += BOOK_LIST.format(
                    list_number=i + ((current_list_page - 1) * 3),
                    book_name=book_in_wishlist["book_name"],
                    book_author=book_in_wishlist["book_author"],
                    book_category=book_category,
                    etb_price=book_in_wishlist["book_etb_price"],
                    usd_price=book_in_wishlist["book_usd_price"],
                    order_page_link=order_page_link,
                    remove_from_wishlist_link=remove_from_wishlist_link,
                )

        return message_body

    def _inline_pagination_btn(self, user_id, current_list_page):
        list_per_page = 3
        total_list = self.wishlist_model.get_total_list(user_id)
        total_list_pages = ceil(total_list / list_per_page)

        back_page = current_list_page - 1
        next_page = current_list_page + 1

        btn_builder = InlineKeyboardBuilder()

        back_btn = InlineKeyboardButton(
            text="⏪  back",
            callback_data=f"wishlist_page:{back_page}",
        )
        page_info_btn = InlineKeyboardButton(
            text=str(current_list_page) + "/" + str(total_list_pages),
            callback_data="disabled_btn",
        )
        next_btn = InlineKeyboardButton(
            text="⏩  next", callback_data=f"wishlist_page:{next_page}"
        )

        if current_list_page == total_list_pages and current_list_page == 1:
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

        btn_builder.add(*pagination_buttons)

        return btn_builder.as_markup()
