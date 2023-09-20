from math import ceil
import logging

# aiogram
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


# project
from telegram_bot.models.book_model import BookModel
from telegram_bot.models.category_model import CategoryModel
from telegram_bot.models.preference_model import PreferenceModel


class PreferenceController:
    book_model = BookModel()
    category_model = CategoryModel()
    preference_model = PreferenceModel()

    step_1_form_header = """
    <b>Step 1: Author Preference</b>\nPlease select your preferred book author from the options below:
    """
    step_2_form_header = """
    <b>Step 2: Genre Preference</b>\nPlease select your preferred book genre from the options below:
    """

    async def send_first_author_pref_page(self, message):
        user_id = str(message.from_user.id)
        form_header = """
        <b>Set your book preferences</b>\nSet your preferences to receive personalized book recommendations from our bot
        """

        await message.answer(text=form_header, parse_mode="html")

        await message.answer(
            text=self.step_1_form_header,
            reply_markup=self._author_listing_inline_btn(user_id=user_id),
            parse_mode="html",
        )

    async def send_first_genre_pref_page(self, query: CallbackQuery):
        user_id = str(query.from_user.id)

        is_filled_author_pref_form = self.preference_model.is_set_preference(
            user_id, preference_type="author"
        )

        if is_filled_author_pref_form:
            await query.message.edit_text(
                text=self.step_2_form_header,
                reply_markup=self._genre_listing_inline_btn(user_id=user_id),
                parse_mode="html",
            )
        else:
            await query.answer(
                text="⚠️ Please choose your preferred book author before proceeding to the next step!",
                show_alert=True,
            )

    async def send_requested_author_pref_page(self, query, requested_page):
        user_id = str(query.from_user.id)

        await query.message.edit_text(
            text=self.step_1_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._author_listing_inline_btn(
                user_id=user_id, current_page=requested_page
            ),
        )

    async def send_requested_genre_pref_page(self, query, requested_page):
        user_id = str(query.from_user.id)

        await query.message.edit_text(
            text=self.step_2_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._genre_listing_inline_btn(
                user_id=user_id, current_page=requested_page
            ),
        )

    async def add_author_to_pref(self, query, author_tempo_id, page_num):
        user_id = str(query.from_user.id)

        # add author to the pref table
        self.preference_model.save_preference(
            user_id=user_id, id=author_tempo_id, preference_type="author"
        )

        # send the updated list
        await query.message.edit_text(
            text=self.step_1_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._author_listing_inline_btn(
                user_id=user_id, current_page=page_num
            ),
        )

    async def add_genre_to_pref(self, query, category_id, page_num):
        user_id = str(query.from_user.id)

        # add author to the pref table
        self.preference_model.save_preference(
            user_id=user_id, id=category_id, preference_type="genre"
        )

        # send the updated list
        await query.message.edit_text(
            text=self.step_2_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._genre_listing_inline_btn(
                user_id=user_id, current_page=page_num
            ),
        )

    async def remove_author_from_pref(self, query, author_tempo_id, page_num):
        user_id = str(query.from_user.id)
        author_name = self.book_model.get_author_by_book_id(author_tempo_id)
        pref_id = self.preference_model.get_pref_id_by_author_name(
            user_id, author_name
        )

        if pref_id:
            # remove author to the pref table
            self.preference_model.remove_preference(
                user_id=user_id, pref_id=pref_id, preference_type="author"
            )

        # send the updated list
        await query.message.edit_text(
            text=self.step_1_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._author_listing_inline_btn(
                user_id=user_id, current_page=page_num
            ),
        )

    async def remove_genre_from_pref(self, query, category_id, page_num):
        user_id = str(query.from_user.id)
        pref_id = self.preference_model.get_pref_id_by_category_id(
            user_id, category_id
        )

        if pref_id:
            # remove author to the pref table
            self.preference_model.remove_preference(
                user_id=user_id, pref_id=pref_id, preference_type="genre"
            )

        # send the updated list
        await query.message.edit_text(
            text=self.step_2_form_header,
            inline_message_id=query.inline_message_id,
            reply_markup=self._genre_listing_inline_btn(
                user_id=user_id, current_page=page_num
            ),
        )

    def _author_listing_inline_btn(self, user_id, current_page=1):
        btn_builder = InlineKeyboardBuilder()

        authors = self.book_model.get_authors()
        preferred_authors = self.preference_model.get_preferred_authors(
            user_id
        )

        inline_buttons = []

        for author in authors:
            if any(
                author[1] == pref_author[1]
                for pref_author in preferred_authors
            ):
                inline_buttons.append("✅ " + str(author[0]))
            else:
                inline_buttons.append(str(author[0]))
        
        list_authors_per_page = 8
        total_list_pages = ceil(len(inline_buttons) / list_authors_per_page)

        limit_start = (current_page - 1) * list_authors_per_page
        limit_end = limit_start + list_authors_per_page

        limited_inline_buttons = inline_buttons[limit_start:limit_end]

        for inline_button_text in limited_inline_buttons:
            if inline_button_text.startswith("✅"):
                author_tempo_id = inline_button_text.split("✅")[-1].strip()
                author_name = self.book_model.get_author_by_book_id(
                    int(author_tempo_id)
                )

                author_name_showing_btn_text = "✅ " + author_name
                callback_data = (
                    f"remove_author_from_pref:{author_tempo_id}:{current_page}"
                )
            else:
                author_tempo_id = inline_button_text
                author_name = self.book_model.get_author_by_book_id(
                    int(author_tempo_id)
                )

                author_name_showing_btn_text = author_name
                callback_data = (
                    f"add_author_to_pref:{author_tempo_id}:{current_page}"
                )

            author_name_showing_btn = InlineKeyboardButton(
                text=author_name_showing_btn_text, callback_data=callback_data
            )
            btn_builder.add(author_name_showing_btn)

        pagination_buttons = self._pagination_buttons(
            current_page, total_list_pages, "author_pref_page"
        )
        btn_builder.add(*pagination_buttons)

        next_step_btn = InlineKeyboardButton(
            text="Next Step",
            callback_data="preference_form_step:genre",
        )
        btn_builder.add(next_step_btn)

        # [author_ls=3,3,3,pag_btn=3/2,genre_prf=1]
        inline_buttons_row_size = self._btn_grid(
            total_list=len(inline_buttons),
            list_per_page=8,
            current_page=current_page,
        )
        pagination_buttons_row_size = [
            len(pagination_buttons),
            1,
        ]
        btn_builder.adjust(
            *inline_buttons_row_size, *pagination_buttons_row_size
        )

        return btn_builder.as_markup()

    def _genre_listing_inline_btn(self, user_id, current_page=1):
        btn_builder = InlineKeyboardBuilder()

        categories = self.category_model.get_categories()
        preferred_genres = self.preference_model.get_preferred_genres(user_id)

        inline_buttons = []

        for category in categories:
            if any(
                category[0] == pref_genre[0] for pref_genre in preferred_genres
            ):
                inline_buttons.append("✅ " + category[1])
            else:
                inline_buttons.append(category[1])

        list_category_per_page = 8
        total_list_pages = ceil(len(inline_buttons) / list_category_per_page)

        limit_start = (current_page - 1) * list_category_per_page
        limit_end = limit_start + list_category_per_page

        limited_inline_buttons = inline_buttons[limit_start:limit_end]

        for inline_button_text in limited_inline_buttons:
            if inline_button_text.startswith("✅"):
                category_name = inline_button_text.split("✅")[-1].strip()
                category_id = self.category_model.get_category_id(
                    category_name
                )

                callback_data = (
                    f"remove_genre_from_pref:{category_id}:{current_page}"
                )
            else:
                category_name = inline_button_text.strip()
                category_id = self.category_model.get_category_id(
                    category_name
                )

                callback_data = (
                    f"add_genre_to_pref:{category_id}:{current_page}"
                )

            category_name_showing_btn = InlineKeyboardButton(
                text=inline_button_text, callback_data=callback_data
            )
            btn_builder.add(category_name_showing_btn)

        pagination_buttons = self._pagination_buttons(
            current_page, total_list_pages, "genre_pref_page"
        )
        btn_builder.add(*pagination_buttons)

        next_step_btn = InlineKeyboardButton(
            text="Submit",
            callback_data="preference_form_step:submit",
        )
        btn_builder.add(next_step_btn)

        # [author_ls=3,3,3,pag_btn=3/2,genre_prf=1]
        inline_buttons_row_size = self._btn_grid(
            total_list=len(inline_buttons),
            list_per_page=8,
            current_page=current_page,
        )
        pagination_buttons_row_size = [
            len(pagination_buttons),
            1,
        ]
        btn_builder.adjust(
            *inline_buttons_row_size, *pagination_buttons_row_size
        )

        return btn_builder.as_markup()

    def _pagination_buttons(self, current_page, total_page, callback_data):
        back_page = current_page - 1
        next_page = current_page + 1

        back_btn = InlineKeyboardButton(
            text=" ⏪ ",
            callback_data=f"{callback_data}:{back_page}",
        )
        page_info_btn = InlineKeyboardButton(
            text=str(current_page) + "/" + str(total_page),
            callback_data="disabled_btn",
        )
        next_btn = InlineKeyboardButton(
            text=" ⏩ ", callback_data=f"{callback_data}:{next_page}"
        )

        if current_page == total_page and current_page == 1:
            pagination_buttons = [page_info_btn]
        elif current_page == 1:
            pagination_buttons = [page_info_btn, next_btn]
        elif current_page == total_page:
            pagination_buttons = [back_btn, page_info_btn]
        else:
            pagination_buttons = [
                back_btn,
                page_info_btn,
                next_btn,
            ]

        return pagination_buttons

    def _btn_grid(self, total_list, list_per_page, current_page):
        total_page = ceil(total_list / list_per_page)
        grid = []

        if current_page < total_page:
            grid.extend([2] * 4)
        elif current_page == total_page:
            remaining_items = total_list % list_per_page

            if remaining_items != 0:
                while remaining_items > 0:
                    if remaining_items >= 2:
                        grid.append(2)
                        remaining_items -= 2
                    else:
                        grid.append(remaining_items)
                        remaining_items = 0
            else:
                grid.extend([2] * 4)

        return grid
