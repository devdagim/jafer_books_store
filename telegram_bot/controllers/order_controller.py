# aiogram
from aiogram.utils.keyboard import InlineKeyboardBuilder

# project
from telegram_bot.template.order_message import (
    ORDER_METHOD_OPTION,
    ORDER_METHOD_ONE,
    ORDER_METHOD_TWO,
    ORDER_METHOD_THERE,
)
from telegram_bot.models.book_model import BookModel


class OrderController:
    book_model = BookModel()

    async def send_order_options(self, message):
        order_option_btn = self._order_option_btn()
        await message.reply(
            ORDER_METHOD_OPTION,
            reply_markup=order_option_btn,
            parse_mode="html",
        )

    async def send_selected_order_option(self, query, data):
        selected_option = int(data["order_option"])
        book_code = data["book_code"]
        option = ""

        if selected_option == 1:
            option = self._visit_store_option(book_code)
        elif selected_option == 2:
            option = self._phone_call_option(book_code)
        elif selected_option == 3:
            option = self._visit_web_option(book_code)

        await query.message.edit_text(
            text=option,
            inline_message_id=str(query.inline_message_id),
            parse_mode="html",
            disable_web_page_preview=True,
        )

    # generate inline btn
    def _order_option_btn(self):
        option_btn_builder = InlineKeyboardBuilder()

        for option_number in range(1, 4):
            option_btn_builder.button(
                text=str(option_number),
                callback_data=f"order_option:{option_number}",
            )

        return option_btn_builder.as_markup()

    # generate templates
    def _visit_store_option(self, book_code):
        book_info = self.book_model.get_book(book_code)

        if book_info:
            phone_call_option = ORDER_METHOD_ONE.format(
                book_name=book_info["book_name"],
                book_author=book_info["book_author"],
            )

            return phone_call_option
        else:
            return "Book Not Found"

    def _phone_call_option(self, book_code):
        book_info = self.book_model.get_book(book_code)

        if book_info:
            phone_call_option = ORDER_METHOD_TWO.format(
                book_name=book_info["book_name"],
                book_author=book_info["book_author"],
            )

            return phone_call_option
        else:
            return "No Book Found"

    def _visit_web_option(self, book_code):
        book_info = self.book_model.get_book(book_code)

        if book_info:
            visit_web_option = ORDER_METHOD_THERE.format(
                jbook_code=book_info["book_code"],
            )

            return visit_web_option
        else:
            return "No Book Found"
